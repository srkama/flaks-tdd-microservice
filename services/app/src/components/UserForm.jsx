import React from 'react';
import { Redirect } from 'react-router-dom';

const UserForm = (props) => {
    if (props.isAuthenticated) {
        return <Redirect to="/" />
    }
    return (
        <div>
            <h1>{props.title}</h1>
            <hr /><br />
            <form onSubmit={props.handleSubmit}>
                <div className="field">
                    <label className="label">Username</label>
                    <div className="control">
                        <input
                            name="username"
                            className="input"
                            type="text"
                            placeholder="Name"
                            value={props.formData.username}
                            onChange={props.handleChange} />
                    </div>
                </div>
                {props.type === 'registration' &&
                    <div className="field">
                        <label className="label">Email</label>
                        <div className="control">
                            <input
                                name="email"
                                className="input"
                                type="text"
                                placeholder="email"
                                value={props.formData.email}
                                onChange={props.handleChange} />
                        </div>
                    </div>
                }
                <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input
                            name="password"
                            className="input"
                            type="password"
                            placeholder="password"
                            value={props.formData.password}
                            onChange={props.handleChange} />
                    </div>
                </div>
                <div className="field is-grouped">
                    <div className="control">
                        <input type="submit" name="submit" className="button is-link" value="Submit" />
                    </div>
                </div>
            </form >
        </div>
    )
}

export default UserForm
