import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const Details = () => {
    const { uid, type } = useParams();
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch(`https://www.swapi.tech/api/${type}/${uid}`)
            .then(res => res.json())
            .then(result => setData(result.result));
    }, [uid, type]);

    if (!data) return <p className="text-center mt-5">Cargando...</p>;

    const imgURL = `https://starwars-visualguide.com/assets/img/${type === 'people' ? 'characters' : type}/${uid}.jpg`;

    return (
        <div className="container mt-4">
            <div className="row">
                <div className="col-md-4">
                    <img src={imgURL} className="img-fluid" alt={data.properties.name} />
                </div>
                <div className="col-md-8">
                    <h2>{data.properties.name}</h2>
                    <ul>
                        {Object.entries(data.properties).map(([key, value]) => (
                            <li key={key}><strong>{key}:</strong> {value}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Details;
