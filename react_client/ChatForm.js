function ChatForm({ onSend, channelEndpoint, channelAuthkey }) {
  // state to store the message input by the user  
  const [message, setMessage] = React.useState("");
  
    // handles form submission when the user sends a message
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (message.trim() === "") return;//ignore empty messages
      const payload = {
        content: message,
        sender: localStorage.getItem('username') || "Unbekannt",
        timestamp: new Date().toISOString()
      };
  
      try {
        //send the message to the channel endpoint
        const response = await fetch(channelEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'authkey ' + channelAuthkey
          },
          body: JSON.stringify(payload)
        });

        //throws an error if request was unsuccesful
        if (!response.ok) {
          throw new Error("Error in sending the message");
        }
        onSend(payload);
        setMessage("");//clear input field after message was sent
      } catch (err) {
        console.error(err);
      }
    };
  
    return (
      <form onSubmit={handleSubmit}>
        {/* input field for typing messages */}
        <input
          type="text"
          placeholder="Your Message"
          value={message}
          onChange={e => setMessage(e.target.value)}
        />
        {/* Submit button to send the message */}
        <button type="submit">Senden</button>
      </form>
    );
  }
  