import (
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/dynamodb"
    "github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"

    "encoding/json"
    "fmt"
    "log"
    "io/ioutil"
    "strconv"
)

// Create struct to hold info about new item
//Sample Json Object Structure
// {
//     "title": "Feeding Sea Lions",
//     "year": 1900,
//     "cast": [
//       "Paul Boyton"
//     ],
//     "genres": [
//       "Short",
//       "Silent"
//     ],
//     "href": "Feeding_Sea_Lions",
//     "extract": "Feeding Sea Lions is short silent film featuring Paul Boyton feeding sea lions at his Sea Lion Park at Coney Island. Boyton is shown feeding the trained sea lions, twelve in number. The sea lions follow Boyton up the steps of the pool and then follow him back into the water. One of them steals food out of the basket. The film was made by Lubin Studios on March 10, 1900."
//   }
type Item struct {
    Year    int
    Title   string
    href    string
	extract string
	cast    [] string
	genres  [] string
}

// Get table items from JSON file
func getItems() []Item {
    raw, err := ioutil.ReadFile("./.movies-1990s.json")
    if err != nil {
        log.Fatalf("Got error reading file: %s", err)
    }

    var items []Item
    json.Unmarshal(raw, &items)
    return items
}

items := getItems()

fmt.Println(items)