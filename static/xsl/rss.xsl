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
      <h1>Emma Juettner RSS Feed</h1>
      <p>This is an RSS feed, which allows you to read the latest updates from this site.
	  You can use the URL of this page to subscribe to this feed in an RSS reader.
	  I also have an <a href="/feed/atom.xml">Atom feed</a> of the same posts, which you may prefer
	  to use if you want to receive the full text of the posts in your RSS reader
	  rather than just the description and a link.</p>
	  <p><a href="/">Return to the main site</a></p>
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