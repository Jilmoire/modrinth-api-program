const axios = require("axios");
const express = require("express");
const exapp = express();

class projectFinder {
    constructor() {
        this.baseURL = "https://api.modrinth.com/v2";
    }

    async searchProjects(options){
        //default value for the passed object
        const {
            queryText,
            facets = [],
            offset = 0,
            limit = 15
        } = options;
        //user indicated valuesw\
        const request = {
            query: queryText,
            facets: JSON.stringify(facets),
            offset,
            limit
        };

        try{
            const recieved = await axios.get(`${this.baseURL}/search`, {params:request});
            return recieved.data;
        }
        catch (error) {
            console.error('Error searching projects:', error.message);
            throw error;
        }
    }
}

exapp.get("/data", async (req, res) => {
    const queryText = req.query.queryText || "fabric";
    const facets = req.query.facets ? JSON.parse(req.query.facets) : [["project_type:mod"], ["categories: fabric"]];
    const offset = req.query.offset ? parseInt(req.query.offset) : 0;
    const limit = req.query.limit ? parseInt(req.query.limit) : 10;
  
    const finder = new projectFinder();
    try {
      const data = await finder.searchProjects({ queryText, facets, offset, limit });
      res.json(data);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });
  


/* testing purposes only */
(async () => {
    const modrinth = new projectFinder();
    try {
      const data = await modrinth.searchProjects({
        queryText: "fabric",
        facets: [["project_type:mod"],["categories: fabric"]],
        offset: 0,
        limit: 1
      });
/*      console.log(JSON.stringify(data));*/
    } catch (error) {
      console.error("Search failed:", error.message);
    }
  })();
/**/



const PORT = process.env.PORT || 3000;
exapp.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});