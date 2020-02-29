from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
class StaticViewSitemap(Sitemap):
    def items(self):
        map = ['index','login','logout',
        'accounts:forgotpassword','accounts:wrongphonenumber',
        'booking:cancellingerror','booking:cantcancell','booking:contractsuccess','booking:notavailablesessions',
            'booking:nosessionerror','booking:cancelsuccess',
        'commonuser:signup',
        'company:createterms','company:termsdetail','company:aboutus','company:contactus','company:faqs',
        'salon:confirmedsalonlist','salon:publiclist',
        'session:publiclist','session:notready','session:todaypubliclist','session:lengtherror',
            'session:boundaryerror','session:noinputerror','session:is_booked','session:logicalerror',
        'sportclub:noaccountdetailerror','sportclub:mapdataset','sportclub:map','sportclub:list',
            'sportclub:publiclist',]
        return map
    def location(self, item):
        return reverse(item)
