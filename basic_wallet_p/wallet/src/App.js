import React, { useState, useEffect } from "react";
// The useState hook holds and sets user state. The useEffect hook performs a pseudo API call that sets “my user” to state.
import "./App.css";
import User from "./components/User";
import { UserContext } from "./contexts/UserContext";

function App() {
  const [user, setUser] = useState(null);
  const [chain, setChain] = useState(null);

  // useEffect(() => {
  //   setUser({ firstName: "John", lastName: "Dough" });
  // }, []);

  return (
    <div className="App">
      <h3 className="App-header">Ree$e Coin</h3>
      <UserContext.Provider value={user}>
        <div className="container">
          <User />
        </div>
      </UserContext.Provider>
    </div>
  );
}

export default App;
