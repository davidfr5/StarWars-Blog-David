import React, { useEffect, useState } from "react";
import Card from "../components/Card.jsx";

const Home = () => {
    const [people, setPeople] = useState([]);
    const [planets, setPlanets] = useState([]);
    const [vehicles, setVehicles] = useState([]);

    useEffect(() => {
        fetch("https://www.swapi.tech/api/people")
            .then(res => res.json())
            .then(data => setPeople(data.results));

        fetch("https://www.swapi.tech/api/planets")
            .then(res => res.json())
            .then(data => setPlanets(data.results));

        fetch("https://www.swapi.tech/api/vehicles")
            .then(res => res.json())
            .then(data => setVehicles(data.results));
    }, []);

    return (
        <div className="container mt-4">
            <h2>Personajes</h2>
            <div className="d-flex overflow-auto">
                {people.map(person => (
                    <Card key={person.uid} item={person} type="people" />
                ))}
            </div>

            <h2>Planetas</h2>
            <div className="d-flex overflow-auto">
                {planets.map(planet => (
                    <Card key={planet.uid} item={planet} type="planets" />
                ))}
            </div>

            <h2>Vehículos</h2>
            <div className="d-flex overflow-auto">
                {vehicles.map(vehicle => (
                    <Card key={vehicle.uid} item={vehicle} type="vehicles" />
                ))}
            </div>
        </div>
    );
};

export default Home;
