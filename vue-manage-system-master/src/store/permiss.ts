import { defineStore } from 'pinia';

interface ObjectList {
    [key: string]: string[];
}

export const usePermissStore = defineStore('permiss', {
    state: () => {
        const defaultList: ObjectList = {
            admin: [
                '0',
                '1',
                '11',
                '12',
                '13',
                '2',
                '21',
                '22',
                '23',
                '24',
                '25',
                '26',
                '27',
                '28',
                '29',
                '291',
                '292',
                '3',
                '31',
                '32',
                '33',
                '34',
                '35',
                '4',
                '41',
                '42',
                '5',
                '7',
                '6',
                '61',
                '62',
                '63',
                '64',
                '65',
                '66',
            ],
            user: ['0', '1', '11', '12', '13'],
            no_access: [],
        };
        const username = localStorage.getItem('vuems_name');
        const access_token = localStorage.getItem('access_token');
        const expires = localStorage.getItem('expires');
        console.log(username, access_token);
        console.log(expires, Date.now());
        if (!access_token) { return { key: defaultList.no_access as string[], } };
        if (!expires) { return { key: defaultList.no_access as string[], } };
        if (parseInt(expires) <= Date.now()) { return { key: defaultList.no_access as string[], } }
        else if (username) {
            return { key: (username == 'admin' ? defaultList.admin : defaultList.user) as string[], defaultList, };
        } else {
            return { key: defaultList.no_access as string[], };
        }
        
    },
    actions: {
        handleSet(val: string[]) {
            this.key = val;
        },
    },
});
