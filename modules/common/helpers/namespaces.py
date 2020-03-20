from lxml import etree

def cleanup_element_namespaces(element_tree):

    # Stylesheet source: https://stackoverflow.com/a/13591813
    xslt_stylesheet = etree.XML('''<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="no"/>

<!-- identity transform for everything else -->
<xsl:template match="/|comment()|processing-instruction()|*|@*">
    <xsl:copy>
      <xsl:apply-templates />
    </xsl:copy>
</xsl:template>

<!-- remove NS from XHTML elements -->
<xsl:template match="*">
    <xsl:element name="{local-name()}">
      <xsl:apply-templates select="@*|node()" />
    </xsl:element>
</xsl:template>


</xsl:stylesheet>''')

    xslt_transform = etree.XSLT(xslt_stylesheet)
    xslt_resultdoc = xslt_transform(element_tree)

    return xslt_resultdoc