import React from 'react'

export default function UserList(props) {
    return (
        <>{
            props.users.map((user) => {
                return (
                    <h4
                        key={user.id}
                        className="box title is-4"
                    >
                        {user.username}
                    </h4>
                )
            })
        }</>
    )
}
