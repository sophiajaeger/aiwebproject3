function ChatForm({ onSend, channelEndpoint, channelAuthkey }) {
    const [message, setMessage] = React.useState("");
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (message.trim() === "") return;
      const payload = {
        content: message,
        sender: localStorage.getItem('username') || "Unbekannt",
        timestamp: new Date().toISOString()
      };
  
      try {
        const response = await fetch(channelEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'authkey ' + channelAuthkey
          },
          body: JSON.stringify(payload)
        });
        if (!response.ok) {
          throw new Error("Error in sending the message");
        }
        onSend(payload);
        setMessage("");
      } catch (err) {
        console.error(err);
      }
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Your Message"
          value={message}
          onChange={e => setMessage(e.target.value)}
        />
        <button type="submit">Senden</button>
      </form>
    );
  }
  