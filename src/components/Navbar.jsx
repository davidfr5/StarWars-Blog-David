import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AppContext } from "../store/appContext.jsx";

const Navbar = () => {
    const { favorites } = useContext(AppContext);

    return (
        <nav className="navbar navbar-dark bg-dark px-4">
            <Link to="/" className="navbar-brand">🚀 Star Wars Blog</Link>
            <Link to="/favorites" className="btn btn-warning">
                Favoritos ({favorites.length})
            </Link>
        </nav>
    );
};

export default Navbar;
