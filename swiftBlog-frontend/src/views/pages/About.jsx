import React from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
function About() {
    return (
        <>
            <Header />

            <section className="pt-4 pb-0">
                <div className="container">
                    <div className="row">
                        <div className="col-xl-9 mx-auto">
                            <h2>Our story</h2>
                            <p className="lead">
                            At Swift Blog, we are passionate about the evolving world of software development. Born out of a classroom project, we aim to share knowledge, insights, and the latest trends in the tech world. From software development tips to deeper explorations of programming languages, frameworks, and methodologies, we cover everything developers need to stay ahead.
                            </p>
                            <p>
                            Our blog is fueled by the idea that knowledge sharing can empower developers of all levels. Whether you're a student just starting out or a seasoned developer refining your skills, we offer tutorials, articles, and resources designed to make your coding journey smoother. We dive deep into topics like agile development, DevOps practices, and cutting-edge tools for web and mobile development. At Swift Blog, we believe that learning is a continuous process, and we strive to help you stay up to date with the latest advancements in the software development industry.
                            </p>
                            <h3 className="mt-4">We do this across:</h3>
                            <ul>
                                <li>Exploring best practices in modern software development and coding standards.</li>
                                <li>Providing insights on emerging technologies, such as artificial intelligence, blockchain, and cloud computing.</li>
                                <li>
                                Offering tutorials and guides on popular programming languages like Python, JavaScript, Java, and more.
                                </li>
                                <li>Sharing tools and frameworks that improve development workflows and efficiency.</li>
                            </ul>
                            <h3 className="mb-3 mt-5">Our team</h3>
                            <div className="row g-4">
                                <div className="col-sm-6 col-lg-3">
                                    <div className="text-center">
                                        <div className="avatar avatar-xxl mb-2">
                                            <img
                                                className="avatar-img rounded-circle"
                                                style={{ width: "100px", height: "100px", objectFit: "cover" }}
                                                src="/default.png"
                                                alt="avatar"
                                            />
                                        </div>
                                        <h5>Maina Isaac</h5>
                                        <p className="m-0">Data Scientist</p>
                                    </div>
                                </div>
                                <div className="col-sm-6 col-lg-3">
                                    <div className="text-center">
                                        <div className="avatar avatar-xxl mb-2">
                                            <img className="avatar-img rounded-circle" style={{ width: "100px", height: "100px", objectFit: "cover" }} src="/default.png" alt="avatar" />{" "}
                                        </div>
                                        <h5>Isaac Maina</h5>
                                        <p className="m-0">Managing Editor</p>
                                    </div>
                                </div>
                                <div className="col-sm-6 col-lg-3">
                                    <div className="text-center">
                                        <div className="avatar avatar-xxl mb-2">
                                            <img
                                                className="avatar-img rounded-circle"
                                                style={{ width: "100px", height: "100px", objectFit: "cover" }}
                                                src="/default.png"
                                                alt="avatar"
                                            />{" "}
                                        </div>
                                        <h5>Maina Isaac</h5>
                                        <p className="m-0">Director Graphics </p>
                                    </div>
                                </div>
                                <div className="col-sm-6 col-lg-3">
                                    <div className="text-center">
                                        <div className="avatar avatar-xxl mb-2">
                                            <img
                                                className="avatar-img rounded-circle"
                                                style={{ width: "100px", height: "100px", objectFit: "cover" }}
                                                src="/default.png"
                                                alt="avatar"
                                            />{" "}
                                        </div>
                                        <h5>Isaac Maina</h5>
                                        <p className="m-0">Editor</p>
                                    </div>
                                </div>
                            </div>
                            {/* Service START */}
                            <h3 className="mb-3 mt-5">What we do</h3>
                            <div className="row">
                                {/* Service item*/}
                                <div className="col-md-6 col-lg-4 mb-4">
                                    <img className="rounded" style={{ width: "100%", height: "170px", objectFit: "cover" }} src="/dp.png" alt="Card image" />
                                    <h4 className="mt-3">Software Development</h4>
                                    <p>We provide in-depth articles about best practices in software development, tools, and techniques that can help developers create better, more efficient software.</p>
                                </div>
                                {/* Service item*/}
                                <div className="col-md-6 col-lg-4 mb-4">
                                    <img className="rounded" style={{ width: "100%", height: "170px", objectFit: "cover" }} src="/dp.png" alt="Card image" />
                                    <h4 className="mt-3">Tutorials and Guides</h4>
                                    <p>From beginners to advanced developers, our tutorials cover everything from setting up your development environment to mastering complex algorithms.</p>
                                </div>
                                {/* Service item*/}
                                <div className="col-md-6 col-lg-4 mb-4">
                                    <img className="rounded" style={{ width: "100%", height: "170px", objectFit: "cover" }} src="/dp.png" alt="Card image" />
                                    <h4 className="mt-3">Tech Trends</h4>
                                    <p> Stay ahead of the curve by reading about the latest trends in software development, AI, cloud technologies, and more.</p>
                                </div>
                            </div>
                            {/* Service END */}
                        </div>{" "}
                        {/* Col END */}
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default About;
