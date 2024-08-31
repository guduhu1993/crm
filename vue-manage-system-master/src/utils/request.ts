import axios, { AxiosInstance, AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

const service: AxiosInstance = axios.create({
    timeout: 5000
});

service.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        return config;
    },
    (error: AxiosError) => {
        console.log(error);
        return Promise.reject();
    }
);

service.interceptors.response.use(
    (response: AxiosResponse) => {
        if (response.status === 200) {
            // const username = localStorage.getItem('vuems_name');
            // const expires = localStorage.getItem('expires');
            // console.log('expires', expires);
            // if (username && expires) {
            //     const result_username = response.data.username;
            //     if (result_username == username) {
            //         const result_expires = response.data.expires;
            //         if (result_expires !== expires) {
            //             console.log('token过期', result_expires, expires);
            //             Promise.reject();
            //         }
            //     }
            // }
            return response;
        } else {
            Promise.reject();
        }
    },
    (error: AxiosError) => {
        console.log(error);
        return Promise.reject();
    }
);

export default service;
