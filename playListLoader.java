/*
 * Psuedocode using java
 * 
 */


 /*
  *  importing dependencies
  */
public class playListLoader {
    
    //config is an instance class to get playlist's folder path
    private botConfig config

    //initialize itself
    public playListLoader(config) {
        this.config = config;
    }
    //returns a list of names of all the text files in a specified folder
    public list<string> getPlaylistName() {
        if(folderExists()) {
            //return array of File objects: the file names turned into string
            //proccess array of File objects to remove suffix: ".txt"
            //put processed strings into a list
            //and return list
        }
        else {
            createFolder();
            //return bool isEmpty()
        }
    }

    public boolean folderExists()
    {
        //return bool files exist in this directory
    }
    
    public void createPlaylist(String name) throws IOException
    {
        //create text file with file name
    }
    
    public void deletePlaylist(String name) throws IOException
    {
        //delete the file in this path that has this name
    }
    
    public void writePlaylist(String name, String text) throws IOException
    {
        //writes text to a file in a specified directory
    }

    public Playlist getPlaylist(String name)
    {
        if(!getPlaylistNames().contains(name))
            return null;
        try
        {
            
            if(folderExists())
            {
                //
                List<String> list = new ArrayList<>();
                Files.readAllLines(/*read into config
                                    -> then playlist folder
                                    -> then txt file
                                    ->  then each line of the file*/)
                {
                    //user input using /commands
                    String s = str.trim();
                    if(s.isEmpty())
                        return;
                    else
                        list.add(s);
                });
            }
            else
            {
                createFolder();
                return null;
            }
        }
        catch(IOException e) {}
    }

    public class Playlist
    {
        String name;
        List<String> items;
        List<AudioTrack> tracks = new LinkedList<>();
        List<PlaylistLoadError> errors = new LinkedList<>();
        boolean loaded = false;
        
        private Playlist(String name, List<String> items)
        {
            this.name = name;
            this.items = items;
        }
        
        public void loadTracks()
        {
            //someway to check if anything is loaded: song, playlist, etc

                //loading the songs ordered songs

                    //load track

                    //load playlist

                    @Override
                    public void noMatches() {}

                    @Override
                    public void loadFailed() {}
                });
            }
        }
        
        public String getName() {}

        public List<String> getItems() {}

        public List<AudioTrack> getTracks() {}
        
        public List<PlaylistLoadError> getErrors() {}
    }

    // debuging 
    public class PlaylistLoadError
    {
        // track index, string item, and exception reason
        int number;
        String item;
        String reason;
    }
}
