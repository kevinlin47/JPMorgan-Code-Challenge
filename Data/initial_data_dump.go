package main

import (
	"strconv"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"

	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	// "strconv"
)

// Create struct to hold info about new item
// Sample Json Object Structure
// "title": "The Adventures of Ford Fairlane",
// "year": 1990,
// "cast": [
//
//	"Andrew Dice Clay",
//	"Wayne Newton",
//	"Priscilla Presley",
//	"Lauren Holly",
//	"Maddie Corman",
//	"Ed O'Neill",
//	"Morris Day",
//	"Tone Loc",
//	"Gilbert Gottfried",
//	"Robert Englund"
//
// ],
// "genres": [
//
//	"Action",
//	"Comedy",
//	"Mystery"
//
// ],
// "href": "The_Adventures_of_Ford_Fairlane",
// "extract": "The Adventures of Ford Fairlane is a 1990 American action comedy mystery film directed by Renny Harlin and written by David Arnott, James Cappe, and Daniel Waters based on a story by Arnott and Cappe. The film stars comedian Andrew Dice Clay as the title character, Ford Fairlane, a \"Rock n' Roll Detective\", whose beat is the music industry in Los Angeles. True to his name, Ford drives a 1957 Ford Fairlane 500 Skyliner in the film.",
// "thumbnail": "https://upload.wikimedia.org/wikipedia/en/a/ac/Fordfairlaneposter.jpg",
// "thumbnail_width": 259,
// "thumbnail_height": 384
// }
type Item struct {
	Title            string
	Year             int
	Cast             []string
	Genres           []string
	Href             string
	Extract          string
	Thumbnail        string
	Thumbnail_width  int
	Thumbnail_height int
}

// Get table items from JSON file
func getItems(fileName string) []Item {
	raw, err := ioutil.ReadFile("./" + fileName)
	if err != nil {
		log.Fatalf("Got error reading file: %s", err)
	}

	var items []Item
	json.Unmarshal(raw, &items)
	return items
}

func main() {
	// Get Movie Objects from the 3 sample data files
	movies1990s := getItems("movies-1990s.json")
	movies2000s := getItems("movies-2000s.json")
	movies2010s := getItems("movies-2010s.json")

	// Create AWS Session
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	// Create DynamoDB client
	svc := dynamodb.New(sess)

	// Add each item to Movies table:
	tableName := "Movies"

	for _, movie := range movies1990s {
		av, err := dynamodbattribute.MarshalMap(movie)

		if err != nil {
			log.Fatalf("Got error marshalling map: %s", err)
		}

		// Create item in table Movies
		input := &dynamodb.PutItemInput{
			Item:      av,
			TableName: aws.String(tableName),
		}

		_, err = svc.PutItem(input)
		if err != nil {
			log.Fatalf("Got error calling PutItem: %s", err)
		}

		year := strconv.Itoa(movie.Year)
		fmt.Println("Successfully added '" + movie.Title + "' (" + year + ") to table " + tableName)
	}
}
