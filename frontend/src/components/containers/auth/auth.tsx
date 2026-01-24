import { useState } from "react";
import Card from "../../small/card/card";
import Button from "../../small/button/button";
import Input from "../../small/input/input";
import { useBookingContext } from "../bookingContext/bookingContext";
import { AUTH_CREDENTIALS } from "./authConfig";
//анимка загрузки
const Spinner = () => (
    <div className="flex justify-center items-center p-4">
        <span className="loading loading-infinity loading-xl text-primary"></span>
    </div>
);

export const AuthContainer = () => {
    const { setIsAuthenticated, login, pass, setLogin,
        setPass, isLoading, setIsLoading, error, setError } = useBookingContext();

    const handleLogin = () => {
        if (login === AUTH_CREDENTIALS.login && pass === AUTH_CREDENTIALS.password) {
            setError(false);
            setIsLoading(true);

            // делей
            setTimeout(() => {
                setIsAuthenticated(true);
                setIsLoading(false);
            }, 1500);
        } else {
            setError(true);
            console.log("Неверный логин или пароль");
        }
    };




    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black/60 z-50 p-6 backdrop-blur-sm">
            {/* Контейнер в стиле BookingCard */}
            <div className="w-full max-w-sm bg-base-200 p-6 rounded-2xl shadow-xl">
                <h3 className="text-xl font-bold mb-6 text-accent-content">Авторизация</h3>

                {error && (
                    <div className="alert alert-error mb-4 py-2 text-sm shadow-lg">
                        <span>Неверный логин или пароль</span>
                    </div>
                )}


                {isLoading ? (
                    <Spinner />
                ) : (
                    <div className="flex flex-col gap-4">
                        <Input
                            label="Логин"
                            placeholder=""
                            variant={error ? "error" : "default"} 
                            className="bg-base-100"
                            onChange={(e) => {
                                setLogin(e.target.value);
                                if (error) setError(false);
                            }}
                            disabled={isLoading}
                        />
                        <Input
                            label="Пароль"
                            type="password"
                            placeholder=""
                            variant={error ? "error" : "default"} 
                            className="bg-base-100"
                            onChange={(e) => {
                                setPass(e.target.value);
                                if (error) setError(false);
                            }}
                            disabled={isLoading}
                        />
                        <div className="mt-2">
                            <Button
                                label="Войти"
                                variant="primary"
                                width="full"
                                size="lg"
                                // onClick={() => {
                                //     if (login === 'admin' && pass === '12345') setIsAuthenticated(true)
                                // }}
                                onClick={handleLogin}
                                shape="rounded"
                                disabled={isLoading}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};
