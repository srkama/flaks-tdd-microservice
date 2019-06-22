import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';

import 'bulma';

import config from './app.config';
import UserList from './components/UserList.jsx';
import Aboutus from './components/Aboutus';
import NavBar from './components/NavBar';
import UserForm from './components/UserForm';

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
            title: 'Test App'
        }
        this.submitHandler = this.submitHandler.bind(this);
        this.changeHandler = this.changeHandler.bind(this);
    }

    componentDidMount() {
        this.getUsers();
    }

    submitHandler(event) {
        event.preventDefault();

        const formType = window.location.pathname.replace('/', '');
        console.log(formType);

        const payload = {
            username: this.state.username,
            password: this.state.password
        }
        if (formType === 'register') {
            payload['email'] = this.state.email
        }
        console.log(payload)
        axios.post(`${config.REACT_API_URL}auth/${formType}`, payload)
            .then(res => {
                this.getUsers();  // new
                this.setState({ username: '', email: '' });  // new
            })
            .catch(err => console.log(err));
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
            handleChange={this.changeHandler}
            handleSubmit={this.submitHandler} />;

        const registerForm = <UserForm
            type='registration'
            title='Registration Form'
            formData={this.state.formData}
            handleChange={this.changeHandler}
            handleSubmit={this.submitHandler} />;

        return (
            <div>
                <NavBar title={this.state.title} />
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
                                </Switch>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        )
    }
}
