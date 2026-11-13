d=open('donate-page/donate-block.html',encoding='utf-8').read()
bud=open('budget-page/budget-block.html',encoding='utf-8').read()
i=d.index('<div id="wat-bud">'); j=d.rindex('</style>',0,d.index('id="wat-wall"'))+8
w=d[i:j]
def rep(s,a,b):
    assert s.count(a)==1,(a[:50],s.count(a)); return s.replace(a,b)
w=rep(w,"WAT_AFTER_FORM(function () {   // (ll) waits for the Pledge form -- see the gate at the top","(function () {")
w=rep(w,"  var DONATIONS_ANCHOR = '#wat-wall';   // the Donations block below this widget; the supporter count links here and smooth-scrolls down to it","  var DONATIONS_ANCHOR = '/donors';   // /budget: the supporter count links to the donor wall")
k=w.rindex("\n});\n</script>"); w=w[:k]+"\n})();\n</script>"+w[k+len("\n});\n</script>"):]
bi=bud.index('<div id="wat-bud">'); bj=bud.index("\n\n<style>\n  /* /budget (2026-10-02)")
open('budget-page/budget-block.html','w',encoding='utf-8').write(bud[:bi]+w+bud[bj:])
