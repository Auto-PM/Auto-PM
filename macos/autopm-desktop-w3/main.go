package main

import (
	_ "embed"
	"log"

	"github.com/wailsapp/wails/v3/pkg/options"

	"github.com/wailsapp/wails/v3/pkg/application"
)

func main() {
	app := application.New(options.Application{
		Name:        "AutoPM",
		Description: "AutoPM",
		Mac: options.Mac{
			ApplicationShouldTerminateAfterLastWindowClosed: true,
		},
	})
	// Create window
	app.NewWebviewWindowWithOptions(&options.WebviewWindow{
		Title:  "AutoPM",
		Width:  600,
		Height: 800,
		Mac: options.MacWindow{
			InvisibleTitleBarHeight: 50,
			//Backdrop:                options.MacBackdropTranslucent,
			TitleBar: options.TitleBarHiddenInset,
		},
		URL: "https://autopm.dev",
	})

	err := app.Run()
	if err != nil {
		log.Fatal(err)
	}
}
