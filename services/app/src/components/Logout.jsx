import React, { Component } from 'react'

export default class Logout extends Component {
    componentDidMount() {
        this.props.logout()
    }

    render() {
        return (
            <p>You are logged out!</p>
        )
    }
}
