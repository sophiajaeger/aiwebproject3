function ChannelList({ onSelectChannel }) {
    {/*creates states that store the channel list and search term input*/}
    const [channels, setChannels] = React.useState([]);
    const [searchTerm, setSearchTerm] = React.useState("");
  
    //fetch the channel list from the server
    React.useEffect(() => {
      fetch("http://vm146.rz.uos.de/hub/channels")//fetch the channel list from the server
        .then(response => response.json())
        .then(data => setChannels(data.channels))
        .catch(err => console.error("Error while loading the channels: ", err));
    }, []);
  
    // filter channels based on the search term
    const filteredChannels = channels.filter(channel =>
      channel.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  
    return (
      <div>
        <h2>Channel Liste</h2>
        {/* input field for searching channels */}
        <input
          type="text"
          placeholder="Search for channels..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />
        {/* display the channel list */}
        <ul>
          {filteredChannels.map((channel, index) => (
            <li key={index} onClick={() => onSelectChannel(channel)}>
              {channel.name} (Typ: {channel.type_of_service})
            </li>
          ))}
        </ul>
      </div>
    );
  }
  