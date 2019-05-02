import React, { Component } from 'react';
import axios from 'axios';
import 'bulma';
import config from './app.config';
import UserList from './components/UserList.jsx';

export default class App extends Component {
  constructor(props) {
    super()
    this.state = {
      users: []
    }
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    axios.get(`${config.REACT_API_URL}users`)
      .then(res => this.setState({ users: res.data['data'] }))
      .catch(err => console.log(err));
  }
  render() {
    console.log(config);
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-one-third">
              <br />
              <h1 className="title is-1">All Users</h1>
              <hr /><br />
              <UserList users={this.state.users} />
            </div>
          </div>
        </div>
      </section>
    )
  }
}
