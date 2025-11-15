package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"slices"
	"strings"

	htmltomarkdown "github.com/JohannesKaufmann/html-to-markdown/v2"
	"github.com/carapace-sh/carapace-spec/pkg/command"
	"github.com/neurosnap/sentences/english"
	"gopkg.in/yaml.v3"
)

func CamelCaseToDash(s string) string {
	re := regexp.MustCompile("([a-z0-9])([A-Z])")
	s = re.ReplaceAllString(s, "${1}-${2}")
	return strings.ToLower(s)
}

type Service struct {
	Version  string `json:"version,omitempty"`
	Metadata struct {
		APIVersion          string   `json:"apiVersion,omitempty"`
		EndpointPrefix      string   `json:"endpointPrefix,omitempty"`
		Protocol            string   `json:"protocol,omitempty"`
		Protocols           []string `json:"protocols,omitempty"`
		ServiceAbbreviation string   `json:"serviceAbbreviation,omitempty"`
		ServiceFullName     string   `json:"serviceFullName,omitempty"`
		ServiceID           string   `json:"serviceId,omitempty"`
		SignatureVersion    string   `json:"signatureVersion,omitempty"`
		UID                 string   `json:"uid,omitempty"`
		XMLNamespace        string   `json:"xmlNamespace,omitempty"`
		Auth                []string `json:"auth,omitempty"`
	} `json:"metadata"`
	Operations    map[string]Operation
	Shapes        map[string]Shape `json:"shapes"`
	Documentation string           `json:"documentation,omitempty"`
}

type Shape struct {
	Type     string            `json:"type,omitempty"`
	Enum     []string          `json:"enum,omitempty"`
	Member   Member            `json:"member"`
	Members  map[string]Member `json:"members"`
	Required []string          `json:"required,omitempty"`
}

type Member struct {
	Shape         string `json:"shape,omitempty"`
	Documentation string `json:"documentation,omitempty"`
	LocationName  string `json:"locationName,omitempty"`
}

type Operation struct {
	Name string `json:"name"`
	HTTP struct {
		Method     string `json:"method"`
		RequestURI string `json:"requestUri"`
	} `json:"http"`
	Input struct {
		Shape string `json:"shape"`
	} `json:"input"`
	Output struct {
		Shape string `json:"shape"`
	} `json:"output"`
	Documentation string `json:"documentation"`
}

func main() {
	services, err := os.ReadDir(os.Args[1])
	if err != nil {
		panic(err.Error())
	}

	cmd := command.Command{
		Name: "aws",
	}

	for _, serviceDir := range services {
		if !serviceDir.IsDir() {
			continue
		}
		path := filepath.Join(os.Args[1], serviceDir.Name())
		versions, err := os.ReadDir(path)
		if err != nil {
			panic(err.Error())
		}
		cmd.Commands = append(cmd.Commands,
			parseService(serviceDir.Name(), filepath.Join(path, versions[len(versions)-1].Name(), "service-2.json")),
		)
	}

	m, err := yaml.Marshal(cmd)
	if err != nil {
		panic(err.Error())
	}
	fmt.Println(string(m))

}

func parseService(name, path string) command.Command {
	tokenizer, err := english.NewSentenceTokenizer(nil)
	if err != nil {
		panic(err.Error())
	}

	content, err := os.ReadFile(path)
	if err != nil {
		panic(err.Error())
	}

	var service Service
	if err := json.Unmarshal(content, &service); err != nil {
		panic(err.Error())
	}

	cmd := command.Command{Name: name}
	cmd.Documentation.Command, _ = htmltomarkdown.ConvertString(service.Documentation)
	if tokens := tokenizer.Tokenize(cmd.Documentation.Command); len(tokens) > 0 {
		cmd.Description = tokens[0].Text
	}

	for _, operation := range service.Operations {
		opdoc, _ := htmltomarkdown.ConvertString(operation.Documentation)
		subCmd := command.Command{
			Name: CamelCaseToDash(operation.Name),
		}
		if tokens := tokenizer.Tokenize(opdoc); len(tokens) > 0 {
			subCmd.Description = tokens[0].Text
		}
		subCmd.Documentation.Command = opdoc
		subCmd.Documentation.Flag = make(map[string]string)

		if shape, ok := service.Shapes[operation.Input.Shape]; ok {
			switch shape.Type {
			case "structure":
				// TODO shape.Member
				for name, member := range shape.Members {
					required := slices.Contains(shape.Required, name)
					memberdoc, _ := htmltomarkdown.ConvertString(member.Documentation)
					subCmd.Documentation.Flag[CamelCaseToDash(name)] = memberdoc
					if tokens := tokenizer.Tokenize(memberdoc); len(tokens) > 0 {
						memberdoc = tokens[0].Text
					}
					subCmd.AddFlag(command.Flag{
						Longhand: "--" + CamelCaseToDash(name),
						Usage:    memberdoc,
						Value:    member.Shape != "Boolean",
						Required: required,
					})
					if member.Shape == "Boolean" {
						subCmd.AddFlag(command.Flag{
							Longhand: "--no-" + CamelCaseToDash(name),
							Usage:    memberdoc,
							Hidden:   true,
							Required: required,
						})
					}
				}
			default:
				// TODO others
			}
		}
		cmd.Commands = append(cmd.Commands, subCmd)
	}
	return cmd
}
