import React from 'react'

export default function AddUser(props) {
    console.log(props);
    const { username, email, handleChange, handleSubmit } = props;
    return (
        <form onSubmit={handleSubmit}>
            <div className="field">
                <label className="label">Name</label>
                <div className="control">
                    <input
                        name="username"
                        className="input"
                        type="text"
                        placeholder="Name"
                        value={username}
                        required
                        onChange={handleChange} />
                </div>
            </div>
            <div className="field">
                <label className="label">Email</label>
                <div className="control">
                    <input
                        name="email"
                        className="input"
                        type="text"
                        placeholder="email"
                        value={email}
                        required
                        onChange={handleChange} />
                </div>
            </div>
            <div className="field is-grouped">
                <div className="control">
                    <input type="submit" name="submit" className="button is-link" value="Submit" />
                </div>
            </div>
        </form >

    )
}
