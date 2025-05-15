import React, { useContext } from "react";
import { AppContext } from "../store/appContext.jsx";
import { Link } from "react-router-dom";

const Favorites = () => {
    const { favorites, removeFavorite } = useContext(AppContext);

    return (
        <div className="container mt-4">
            <h2>Favoritos</h2>
            {favorites.length === 0 ? (
                <p>No hay favoritos aún.</p>
            ) : (
                <div className="row">
                    {favorites.map(item => {
                        const imgURL = `https://starwars-visualguide.com/assets/img/${item.type === 'people' ? 'characters' : item.type}/${item.uid}.jpg`;

                        return (
                            <div key={item.uid + item.type} className="col-md-4 mb-3">
                                <div className="card">
                                    <img
                                        src={imgURL}
                                        className="card-img-top"
                                        alt={item.name}
                                        onError={(e) => { e.target.src = "https://via.placeholder.com/400x300?text=Sin+imagen"; }}
                                    />
                                    <div className="card-body">
                                        <h5 className="card-title">{item.name}</h5>
                                        <Link
                                            to={`/${item.type}/${item.uid}`}
                                            className="btn btn-primary me-2"
                                        >
                                            Ver más
                                        </Link>
                                        <button
                                            className="btn btn-danger"
                                            onClick={() => removeFavorite(item)}
                                        >
                                            Eliminar
                                        </button>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default Favorites;
