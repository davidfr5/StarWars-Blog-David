import React, { createContext, useState, useEffect } from "react";

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
    const [favorites, setFavorites] = useState([]);

    useEffect(() => {
        fetch("https://animated-space-zebra-jwvvqvprw9xh5vwr-5000.app.github.dev/api/users/favorites")
            .then(res => res.json())
            .then(data => {
                setFavorites(data);
            })
            .catch(err => console.error("Error loading favorites from API:", err));
    }, []);

    const addFavorite = async (item) => {
        const exists = favorites.find(fav => fav.uid === item.uid && fav.type === item.type);
        if (exists) {
            alert(`${item.name} ya está en tus favoritos.`);
            return;
        }

        const url = `https://animated-space-zebra-jwvvqvprw9xh5vwr-5000.app.github.dev/api/favorite/${item.type}/${item.uid}`;
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data.message);
                setFavorites([...favorites, item]);
            } else {
                const errorData = await response.json();
                console.error("Error adding favorite to backend:", errorData.message);
                alert(`Error al añadir ${item.name} a favoritos: ${errorData.message}`);
            }
        } catch (error) {
            console.error("Network error adding favorite:", error);
            alert("Error de red al añadir favorito.");
        }
    };

    const removeFavorite = async (item) => {
        const url = `https://animated-space-zebra-jwvvqvprw9xh5vwr-5000.app.github.dev/api/favorite/${item.type}/${item.uid}`;
        try {
            const response = await fetch(url, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data.message);
                setFavorites(favorites.filter(fav => !(fav.uid === item.uid && fav.type === item.type)));
            } else {
                const errorData = await response.json();
                console.error("Error removing favorite from backend:", errorData.message);
                alert(`Error al eliminar ${item.name} de favoritos: ${errorData.message}`);
            }
        } catch (error) {
            console.error("Network error removing favorite:", error);
            alert("Error de red al eliminar favorito.");
        }
    };

    return (
        <AppContext.Provider value={{ favorites, addFavorite, removeFavorite }}>
            {children}
        </AppContext.Provider>
    );
};