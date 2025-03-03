function UserLogin() {
    // state to store the username
    const [name, setName] = React.useState(localStorage.getItem('username') || "");
  
    // handles the enter key event in the input field
    const handleKeyDown = (e) => {
      if (e.key === "Enter") {
        const enteredName = e.target.value;
        setName(enteredName); // update state with the entered name
        localStorage.setItem('username', enteredName);
      }
    };
    
    //displays a greeting if a username is set and clear name if someone logs out
    if (name) {
      return (
        <div>
          <h2>Hi {name}</h2>
          <button onClick={() => {
            setName("");
            localStorage.removeItem('username');
          }}>Logout</button>
        </div>
      );
    }
  
    // if no username is set, display an input field for the user to enter their name
    return (
      <div>
        <h2>Enter yur Name:</h2>
        <input type="text" onKeyDown={handleKeyDown} placeholder="Dein Name" />
      </div>
    );
  }
  