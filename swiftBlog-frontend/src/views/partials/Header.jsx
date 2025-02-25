import React from "react";
import { Link } from "react-router-dom";
import { useAuthStore } from "../../store/auth";

function Header() {
    const [isLoggedIn, user] = useAuthStore((state) => [state.isLoggedIn, state.user]);
    return (
        <header className="navbar-dark bg-dark navbar-sticky header-static">
            <nav className="navbar navbar-expand-lg">
                <div className="container">
                    <Link className="navbar-brand" to="/">
                        <h2>SWIFTBLOG</h2>
                    </Link>
                    <button className="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="h6 d-none d-sm-inline-block text-white">Menu</span>
                        <span className="navbar-toggler-icon" />
                    </button>
                    <div className="collapse navbar-collapse" id="navbarCollapse">
                        {/* <div className="nav mt-3 mt-lg-0 px-4 flex-nowrap align-items-center">
                            <div className="nav-item w-100">
                                <form className="rounded position-relative">
                                    <input className="form-control pe-5 bg-light" type="search" placeholder="Search Articles" aria-label="Search" />
                                    <Link to={"/search/"} className="btn bg-transparent border-0 px-2 py-0 position-absolute top-50 end-0 translate-middle-y" type="submit">
                                        <i className="bi bi-search fs-5"> </i>
                                    </Link>
                                </form>
                            </div>
                        </div> */}
                        <ul className="navbar-nav navbar-nav-scroll ms-auto">
                            <li className="nav-item dropdown">
                                <Link className="nav-link active" to="/">
                                    Home
                                </Link>
                            </li>
                            <li className="nav-item dropdown">
                                <Link className="nav-link active" to="/about/">
                                     About
                                </Link>
                            </li>
                            <li className="nav-item dropdown">
                                <Link className="nav-link active" to="/contact/">
                                     Contact
                                </Link>
                            </li>
                            {/* <li className="nav-item">
                                {isLoggedIn() ? (
                                    <>
                                        <Link to={"/dashboard/"} className="btn btn-secondary" href="dashboard.html">
                                            Dashboard <i className="bi bi-grid-fill"></i>
                                        </Link>
                                        <Link to={"/logout/"} className="btn btn-danger ms-2" href="dashboard.html">
                                            Logout <i className="fas fa-sign-out-alt"></i>
                                        </Link>
                                    </>
                                ) : (
                                    <>
                                        <Link to={"/register/"} className="btn btn-success" href="dashboard.html">
                                            Register <i className="fas fa-user-plus"></i>
                                        </Link>
                                        <Link to={"/login/"} className="btn btn-success ms-2" href="dashboard.html">
                                            Login <i className="fas fa-sign-in-alt"></i>
                                        </Link>
                                    </>
                                )}
                            </li> */}
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Header;
