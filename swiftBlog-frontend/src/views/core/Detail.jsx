import React, { useState, useEffect } from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { Link, useParams } from "react-router-dom";

import apiInstance from "../../utils/axios";
import moment from "moment";
import Toast from "../../plugin/Toast";

function Detail() {
    const [post, setPost] = useState([]);
    const [tags, setTags] = useState([]);
    const [createComment, setCreateComment] = useState({ full_name: "", email: "", comment: "" });

    const param = useParams();

    const fetchPost = async () => {
        const response = await apiInstance.get(`post/detail/${param.slug}/`);
        setPost(response.data);

        const tagArray = response.data?.tags?.split(",");
        setTags(tagArray);
    };

    useEffect(() => {
        fetchPost();
    }, []);

    const handleCreateCommentChange = (event) => {
        setCreateComment({
            ...createComment,
            [event.target.name]: event.target.value,
        });
    };

    const handleCreateCommentSubmit = async (e) => {
        e.preventDefault();

        console.log(post.id);
        console.log(createComment.full_name);
        console.log(createComment.email);
        console.log(createComment.comment);

        const jsonData = {
            post_id: post?.id,
            name: createComment.full_name,
            email: createComment.email,
            comment: createComment.comment,
        };

        const response = await apiInstance.post(`post/comment-post/`, jsonData);
        console.log(response);
        fetchPost();
        Toast("success", "Comment Posted.", "");
        setCreateComment({
            full_name: "",
            email: "",
            comment: "",
        });
    };

    const handleLikePost = async()=> {
        const json = {
            user_id: 1,
            post_id: post?.id,

        };
        const response = await apiInstance.post(`post/like-post/`, json);
        console.log(response.data);
        Toast("success", response.data.message);
        fetchPost();
    }

    return (
        <>
            <Header />
            <section className=" mt-5">
                <div className="container">
                    <div className="row">
                        <div className="col-12">
                            <a href="#" className="badge bg-danger mb-2 text-decoration-none">
                                <i className="small fw-bold " />
                                {post.category?.title}
                            </a>
                            <h1 className="text-center">{post.title}</h1>
                        </div>
                    </div>
                </div>
            </section>

            <section className="pt-0">
                <div className="container position-relative" data-sticky-container="">
                    <div className="row">
                        <div className="col-lg-2">
                            <div className="text-start text-lg-center mb-5" data-sticky="" data-margin-top={80} data-sticky-for={991}>
                                <div className="position-relative">
                                    <div className="avatar avatar-xl">
                                        <img className="avatar-img" style={{ width: "100px", height: "100px", objectFit: "cover", borderRadius: "50%" }} src={post.profile?.image} alt="avatar" />
                                    </div>
                                    <a href="#" className="h5 fw-bold text-dark text-decoration-none mt-2 mb-0 d-block">
                                        {post.profile?.full_name}
                                    </a>
                                    <p>{post.profile?.bio}</p>
                                </div>

                                <hr className="d-none d-lg-block " />

                                <ul className="list-inline list-unstyled">
                                    <li className="list-inline-item d-lg-block my-lg-2 text-start">
                                        <i className="fas fa-calendar"></i> {moment(post.date).format("DD MMM, YYYY")}
                                    </li>
                                    <li className="list-inline-item d-lg-block my-lg-2 text-start">
                                        <a href="#" className="text-body">
                                            <i className="fas fa-heart me-1" />
                                        </a>
                                        {post.likes?.length} Likes
                                    </li>
                                    <li className="list-inline-item d-lg-block my-lg-2 text-start">
                                        <i className="fas fa-eye me-1" />
                                        {post.view} Views
                                    </li>
                                </ul>
                                <button onClick={handleLikePost} className="btn btn-success">
                                    <i className="fas fa-thumbs-up"></i>
                                </button>
                            </div>
                        </div>
                        {/* Left sidebar END */}
                        {/* Main Content START */}
                        <div className="col-lg-10 mb-5">
                            <p dangerouslySetInnerHTML={{ __html: post.description }}></p>
                            <div>
                                <h3>{post.comments?.length} comments</h3>
                                {post.comments?.map((c, index) => (
                                    <div className="my-4 d-flex bg-light p-3 mb-3 rounded">
                                        <div>
                                            <div className="mb-2">
                                                <h5 className="m-0">{c.name}</h5>
                                                <span className="me-3 small">{moment(c.date).format("DD MMM, YYYY")}</span>
                                            </div>
                                            <p className="fw-bold">{c.comment}</p>
                                            {c.reply !== null && <p className="">Reply: {c.reply}</p>}
                                        </div>
                                    </div>
                                ))}
                            </div>
                            {/* Comments END */}
                            {/* Reply START */}
                            <div className="bg-light p-3 rounded">
                                <h3 className="fw-bold">Comment Below</h3>
                                <form className="row g-3 mt-2" onSubmit={handleCreateCommentSubmit}>
                                    <div className="col-md-6">
                                        <label className="form-label">Name *</label>
                                        <input onChange={handleCreateCommentChange} name="full_name" value={createComment.full_name} type="text" className="form-control" aria-label="First name" />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Email *</label>
                                        <input onChange={handleCreateCommentChange} name="email" value={createComment.email} type="email" className="form-control" />
                                    </div>
                                    <div className="col-12">
                                        <label className="form-label">Write Comment *</label>
                                        <textarea onChange={handleCreateCommentChange} name="comment" value={createComment.comment} className="form-control" rows={4} />
                                    </div>
                                    <div className="col-12">
                                        <button type="submit" className="btn btn-primary">
                                            Post comment
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default Detail;
