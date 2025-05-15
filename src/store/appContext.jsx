import React, { createContext, useState } from "react";

export const AppContext = createContext();

// Creacion del provider
export const AppProvider = ({ children }) => {
    const [favorites, setFavorites] = useState([]);

    const addFavorite = (item) => {
        const exists = favorites.find(fav => fav.uid === item.uid && fav.type === item.type);
        if (!exists) {
            setFavorites([...favorites, item]);
        }
    };

    const removeFavorite = (item) => {
        setFavorites(favorites.filter(fav => !(fav.uid === item.uid && fav.type === item.type)));
    };

    return (
        <AppContext.Provider value={{ favorites, addFavorite, removeFavorite }}>
            {children}
        </AppContext.Provider>
    );
};
