function UserLogin() {
    const [name, setName] = React.useState(localStorage.getItem('username') || "");
  
    const handleKeyDown = (e) => {
      if (e.key === "Enter") {
        const enteredName = e.target.value;
        setName(enteredName);
        localStorage.setItem('username', enteredName);
      }
    };
  
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
  
    return (
      <div>
        <h2>Enter yur Name:</h2>
        <input type="text" onKeyDown={handleKeyDown} placeholder="Dein Name" />
      </div>
    );
  }
  