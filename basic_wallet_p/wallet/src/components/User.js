import React, { useContext } from "react";
import { UserContext } from "../contexts/UserContext";

function User() {
  const user = useContext(UserContext);

  return (
    <div className="profile">
      {user.lastName}, {user.firstName}
    </div>
  );
}

export default User;
