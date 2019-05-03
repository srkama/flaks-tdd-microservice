let config = {
    REACT_API_URL: process.env.REACT_APP_USERS_SERVICE_URL ? process.env.REACT_APP_USERS_SERVICE_URL : "http://localhost/"
};

module.exports = config;
