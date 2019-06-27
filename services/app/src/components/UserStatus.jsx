import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import axios from 'axios';
import config from '../app.config';

export default class UserStatus extends Component {
    state = {
        user: '',
        error: false
    }

    componentDidMount() {
        this.checkStatus()
    }

    checkStatus = () => {

        const options = {
            url: `${config.REACT_API_URL}auth/status`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.auth_token}`
            }
        };

        axios(options)
            .then((res) => {
                console.log(res.data);
                this.setState({ user: res.data.data })
                console.log(this.state);

            })
            .catch((err) => { this.setState({ error: true }) });

    }

    render() {

        if (this.props.isAuthenticated || this.state.error) {
            return <p>You must be logged in to view this. Click <Link to="/login">here</Link> to log back in.</p>
        }

        return (
            <div>
                <ul>
                    <li><strong>User ID:</strong> {this.state.user.id}</li>
                    <li><strong>Email:</strong> {this.state.user.email}</li>
                    <li><strong>Username:</strong> {this.state.user.username}</li>
                </ul>
            </div>
        )
    }
}
