const BASE_URL = 'http://' + window.location.hostname + ':8000/endpoints/'

export const createEndpoint = async(endpointData) => {
    let url = BASE_URL
    const rawResponse = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(endpointData),
    })
    const response = await rawResponse;
    return response
};

export const getEndpoints = async() => {
    return fetch(BASE_URL).then( (res) => res.json() );
};