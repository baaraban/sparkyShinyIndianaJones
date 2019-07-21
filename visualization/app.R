---
  title: "Artifacts Flow Visualized"
author: "Nazariy Perepichka"
date: "July 10, 2019"
output: html_document
library(shiny)
library(leaflet)
library(RColorBrewer)
library(ggplot2)
library(dplyr)

## Data loading

DATA_PATH = 'data/for_visual.csv'
data <- read.csv(DATA_PATH)

data <- data %>%
  arrange(year) %>%
  group_by(artifact_name) %>%
  filter(n() > 1)

data$lat_start <- ave(data$lat, data$artifact_name, FUN=function(x) c(0, x))
data$lon_start <- ave(data$lon, data$artifact_name, FUN=function(x) c(0, x))

data <- data %>%
  filter(lon_start == 0 & lat_start == 0) 


## UI calculations

min_year <- min(data$year) 
max_year <- if (max(data$year) < 2019) max(data$year) else 2019


## User interface

ui <- navbarPage("artifacts", id='nav',
                 tabPanel("Interactive map",
                          div(class="outer",
                              tags$head(
                                # Include our custom CSS
                                includeCSS("styles/index.css")
                              ),
                              leafletOutput("map", width="100%", height="100%"),
                              absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                            draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                            width = 450, height = "auto",
                                            fluidRow(
                                              column(12, sliderInput("year_range", label=h3("Years"), min=min_year, max=max_year,  c(min_year, max_year)))
                                            )
                              )
                          )
                 )
)

server <- function(input, output, session) {
  
  artifactsInYears <- reactive({
    year_range = input$year_range
    filter(data, year >= year_range[1] & year <= year_range[2])
  })
  
  output$map <- renderLeaflet({
    directions = artifactsInYears()
    
    pal <- colorNumeric(palette = "Accent", domain = directions$year, n = 5)
    
    leaflet() %>%
      addProviderTiles(providers$Stamen.TonerLite,
                       options = providerTileOptions(noWrap = TRUE)
      ) %>%
      addPolylines(
        data = directions,
        weight = 1,
        opacity = 0.5,
        lng = ~ c(lon_start, lon),
        lat = ~ c(lat_start, lat),
        color = ~pal(year)
        #)
        # This approach to add colors is actually bad
      ) %>%
      addLegend(data = directions, pal = pal, values = ~year, opacity = 0.5)
  })
  
}

shinyApp(ui, server)
