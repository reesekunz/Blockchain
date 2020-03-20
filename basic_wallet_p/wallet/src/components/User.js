import React, { useContext, useState, useEffect } from "react";
import { UserContext } from "../contexts/UserContext";
import axios from "axios";

function User(props) {
  const userContext = useContext(UserContext);
  const [value, setValue] = useState(null);
  const handleSubmit = event => {
    // useEffect(() => {
    event.preventDefault();
    //   const proxyurl = "https://cors-anywhere.herokuapp.com/";
    //   const url = "http://localhost:5000/chain";
    axios
      .get("http://localhost:5000/chain")
      .then(response => userContext.setChain(response.data.chain))
      .catch(error => console.log("error =", error));
    // }, []);
  };
  const handleChange = event => {
    setValue(event.target.value);
  };
  return (
    <div className="profile">
      <h3>Get Wallet</h3>
      <input
        value={value}
        type="text"
        name="username"
        placeholder="username"
        onChange={handleChange}
      ></input>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default User;
