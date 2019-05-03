import React, { Component } from 'react';
import axios from 'axios';
import 'bulma';
import config from './app.config';
import UserList from './components/UserList.jsx';
import AddUser from './components/AddUser';

export default class App extends Component {
  constructor(props) {
    super()
    this.state = {
      users: [],
      username: '',
      email: ''
    }
    this.submitHandler = this.submitHandler.bind(this);
    this.changeHandler = this.changeHandler.bind(this);
  }

  componentDidMount() {
    this.getUsers();
  }

  submitHandler(event) {
    event.preventDefault();
    const payload = {
      username: this.state.username,
      email: this.state.email
    }
    axios.post(`${config.REACT_API_URL}users`, payload)
      .then(res => {
        this.getUsers();  // new
        this.setState({ username: '', email: '' });  // new
      })
      .catch(err => console.log(err));
  }

  changeHandler(event) {
    this.setState({ [event.target.name]: event.target.value })
  }

  getUsers() {
    axios.get(`${config.REACT_API_URL}users`)
      .then(res => this.setState({ users: res.data['data'] }))
      .catch(err => console.log(err));
  }
  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br />
              <h1 className="title is-1">All Users</h1>
              <hr /><br />
              <AddUser
                username={this.state.username}
                email={this.state.email}
                handleSubmit={this.submitHandler}
                handleChange={this.changeHandler} />
              <hr /><br />
              <UserList users={this.state.users} />
            </div>
          </div>
        </div>
      </section>
    )
  }
}
