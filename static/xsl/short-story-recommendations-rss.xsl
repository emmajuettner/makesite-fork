<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
  <head>
    <title><xsl:value-of select="rss/channel/title"/> (RSS Feed)</title>
    <style type="text/css">
    @import url(/css/rss.css);
    </style>
  </head>
  <body>
    <div id="explanation">
      <h1>Emma's Short Story Recommendations RSS Feed</h1>
      <p>This is an RSS feed, which allows you to read the latest updates from my Short Stories Recommendations page.
	  You can use the URL of this page to subscribe to this feed in an RSS reader.</p>
	  <p><a href="/short-story-recommendations">Return to the main page</a></p>
    </div>
    <div id="content">
      <xsl:for-each select="rss/channel/item">
	  <hr />
      <div class="article">
        <h2><a href="{link}" rel="bookmark"><xsl:value-of select="title"/></a></h2>
		<p><xsl:value-of select="substring-before(pubDate, 'T')"/></p>
        <p><xsl:value-of select="description"/></p>
      </div>
      </xsl:for-each>
    </div>
  </body>
</html>
</xsl:template>
</xsl:stylesheet>
