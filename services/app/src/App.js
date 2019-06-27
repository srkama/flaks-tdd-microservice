import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';

import 'bulma';

import config from './app.config';
import UserList from './components/UserList.jsx';
import Aboutus from './components/Aboutus';
import NavBar from './components/NavBar';
import UserForm from './components/UserForm';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';

export default class App extends Component {
    constructor(props) {
        super()
        this.state = {
            users: [],
            formData: {
                'username': '',
                'email': '',
                'password': ''
            },
            title: 'Test App',
            isAuthenticated: false
        }
        this.submitHandler = this.submitHandler.bind(this);
        this.changeHandler = this.changeHandler.bind(this);
        this.logoutHandler = this.logout.bind(this);
    }

    componentDidMount() {
        this.getUsers();
    }

    submitHandler(event) {
        event.preventDefault();

        const formType = window.location.pathname.replace('/', '');

        const payload = {
            username: this.state.formData.username,
            password: this.state.formData.password
        }
        if (formType === 'registration') {
            payload['email'] = this.state.formData.email
        }
        axios.post(`${config.REACT_API_URL}auth/${formType}`, payload)
            .then(res => {
                this.setState(
                    {
                        formData: {
                            'username': '',
                            'email': '',
                            'password': ''
                        },
                        isAuthenticated: true
                    });
                window.localStorage.setItem('auth_token', res.data['token']);
                this.getUsers()
            })
            .catch(err => {
                this.setState({ isAuthenticated: false })
            });
    }

    changeHandler(event) {
        let obj = this.state.formData
        obj[event.target.name] = event.target.value;
        this.setState({ formData: obj });
    }

    getUsers() {
        axios.get(`${config.REACT_API_URL}users`)
            .then(res => this.setState({ users: res.data['data'] }))
            .catch(err => console.log(err));
    }

    logout() {
        window.localStorage.clear()
        this.setState({ isAuthenticated: false })
    }

    render() {
        const userSection = <div>
            <h1 className="title is-1">All Users</h1>
            <hr /><br />
            <UserList users={this.state.users} />
        </div>

        const loginForm = <UserForm
            type='login'
            title='Login Form'
            formData={this.state.formData}
            isAuthenticated={this.state.isAuthenticated}
            handleChange={this.changeHandler}
            handleSubmit={this.submitHandler} />;

        const registerForm = <UserForm
            type='registration'
            title='Registration Form'
            isAuthenticated={this.state.isAuthenticated}
            formData={this.state.formData}
            handleChange={this.changeHandler}
            handleSubmit={this.submitHandler} />;

        const logout = <Logout logout={this.logoutHandler}></Logout>

        return (
            <div>
                <NavBar title={this.state.title} isAuthenticated={this.state.isAuthenticated} />
                <section className="section">
                    <div className="container">
                        <div className="columns">
                            <div className="column is-half">
                                <br />
                                <Switch>
                                    <Route exact path="/" render={() => userSection} />
                                    <Route exact path="/aboutus" component={Aboutus} />
                                    <Route exact path="/registration" render={() => registerForm} />
                                    <Route exact path="/login" render={() => loginForm} />
                                    <Route exact path="/logout" render={() => logout} />
                                    <Route exact path='/status' render={() => <UserStatus isAuthenticated={this.state.isAuthenticated} />} />
                                </Switch>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        )
    }
}
