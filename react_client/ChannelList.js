function ChannelList({ onSelectChannel }) {
    const [channels, setChannels] = React.useState([]);
    const [searchTerm, setSearchTerm] = React.useState("");
  
    React.useEffect(() => {
      fetch("http://vm146.rz.uos.de/hub/channels")
        .then(response => response.json())
        .then(data => setChannels(data.channels))
        .catch(err => console.error("Error while loading the channels: ", err));
    }, []);
  
    const filteredChannels = channels.filter(channel =>
      channel.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  
    return (
      <div>
        <h2>Channel Liste</h2>
        <input
          type="text"
          placeholder="Search for channels..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />
        <ul>
          {filteredChannels.map((channel, index) => (
            <li key={index} onClick={() => onSelectChannel(channel)}>
              {channel.name} (Typ: {channel.type_of_service})
              {/* Hier könnt ihr optional den Activity Indicator einfügen */}
            </li>
          ))}
        </ul>
      </div>
    );
  }
  