import React, { useEffect, useState } from "react";
import Card from "../components/Card.jsx";

const Home = () => {
    const [people, setPeople] = useState([]);
    const [planets, setPlanets] = useState([]);
    const [vehicles, setVehicles] = useState([]);

    useEffect(() => {
        fetch("https://animated-space-zebra-jwvvqvprw9xh5vwr-5000.app.github.dev/api/people")
            .then(res => res.json())
            .then(data => setPeople(data))
            .catch(err => console.error("Error fetching people:", err));

        fetch("https://animated-space-zebra-jwvvqvprw9xh5vwr-5000.app.github.dev/api/planets")
            .then(res => res.json())
            .then(data => setPlanets(data))
            .catch(err => console.error("Error fetching planets:", err));

        fetch("https://www.swapi.tech/api/vehicles")
            .then(res => res.json())
            .then(data => setVehicles(data.results))
            .catch(err => console.error("Error fetching vehicles:", err));
    }, []);

    return (
        <div className="container mt-4">
            <h2>Personajes</h2>
            <div className="d-flex overflow-auto">
                {people.map(person => (
                    <Card key={person.id} item={{uid: person.id, name: person.name}} type="people" />
                ))}
            </div>

            <h2>Planetas</h2>
            <div className="d-flex overflow-auto">
                {planets.map(planet => (
                    <Card key={planet.id} item={{uid: planet.id, name: planet.name}} type="planets" />
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