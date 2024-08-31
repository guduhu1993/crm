import request from '../utils/request';

////////////////////////////// 人才 ////////////////////////////////////////////////////////
export const fetchData = () => {
    console.log('token---',localStorage.getItem('access_token'));
    return request({
        // url: './mock/table.json',
        url: 'http://localhost:8000/providers',
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            // 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI1Njk5OTkwfQ.Ed2Z_VmHBs1LWx6dH9JRl7TZkiis1voILCdsu5JjXjo'
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    });
};
export const modifyProvidersData = (data: any) => {
    console.log('修改人才', data);
    return request({
        url: 'http://localhost:8000/modify_provider',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        data: data
    });
};
export const addProvidersData = (data: any) => {
    console.log('添加人才', data);
    return request({
        url: 'http://localhost:8000/provider',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        data: data
    });
};

export const deleteProvider = (provider_id) => {
    return request({
        url: 'http://localhost:8000/delete_provider?provider_id=' + provider_id,
        method: 'get',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    });
};

////////////////////////////// 用户信息 ////////////////////////////////////////////////////////
export const fetchUserData = () => {
    return request({
        url: './mock/user.json',
        method: 'get'
    });
};

export const fetchRoleData = () => {
    return request({
        url: './mock/role.json',
        method: 'get'
    });
};


////////////////////////////// 登陆注册 ////////////////////////////////////////////////////////
export const _register = (data: any) => {
    return request({
        url: 'http://localhost:8000/register/?phone=' + data.phone,
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
        },
        data: { 
            username: data.username, 
            password: data.password
         }
    });
};
export const _login = (data: any) => {
    return request({
        url: 'http://localhost:8000/token',
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json'
        },
        data: data
    });
};

export const _change_password = (data: any) => {
    return request({
        url: 'http://localhost:8000/change_password',
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        data: data
    });
};

export const uploadImage = (flag:string, data: string) => {
    return request({
        url: 'http://localhost:8000/upload_image?'+'flag='+flag+'&image_base64=' + data,
        method: 'get',
        headers: {
            // 'Content-Type': 'application/json',
            'accept': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
    });
}