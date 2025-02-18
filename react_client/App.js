function App() {
    // Create a state variable "selectedChannel" to keep track of the channel the user selects.
  // Initially, no channel is selected, so it's set to null
    const [selectedChannel, setSelectedChannel] = React.useState(null);
  
    return (
      <div>
        {/* Render the UserLogin component to allow the user to enter their name. */}
        <UserLogin />
        <ChannelList onSelectChannel={setSelectedChannel} />
        {selectedChannel ? (
          <ChatWindow 
            channelEndpoint={selectedChannel.endpoint} 
            channelAuthkey={selectedChannel.authkey}
          />
        ) : (
          <p>Please select a channel.</p>
        )}
      </div>
    );
  }
  
  // Render the App component into the DOM element with the id "root"
  ReactDOM.render(<App />, document.getElementById('root'));
  