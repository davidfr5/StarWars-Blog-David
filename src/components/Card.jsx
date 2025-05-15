import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AppContext } from "../store/appContext.jsx";

const Card = ({ item, type }) => {
    const { addFavorite } = useContext(AppContext);

    const imgURL = `https://starwars-visualguide.com/assets/img/${type === 'people' ? 'characters' : type}/${item.uid}.jpg`;

    return (
        <div className="card card-custom">
            <img src={imgURL} className="card-img-top" alt={item.name} />
            <div className="card-body">
                <h5 className="card-title">{item.name}</h5>
                <Link to={`/${type}/${item.uid}`} className="btn btn-primary btn-ver-mas">Ver más</Link>
                <button className="btn btn-outline-warning" onClick={() => addFavorite({ ...item, type })}>
                    ⭐
                </button>
            </div>
        </div>
    );
};

export default Card;
