# Individual Owner Acquisition Plan for nature-office

## Target Vehicle Profile
**Primary Target:** Ford Transit T-250/T-350 AWD Medium/High Roof (2020-2025)
**Secondary Targets:** Mercedes Sprinter AWD/4x4 High Roof, Ram ProMaster High Roof
**Location Focus:** Calgary, Edmonton, and surrounding Alberta corridor

**Ideal Owner Profile:**
- Owns vehicle outright or has significant equity
- Vehicle sits idle 3+ days/week (weekend warrior, seasonal use, business asset)
- Has invested in upgrades (solar, battery, insulation, connectivity)
- Values professional maintenance and insurance coverage
- Open to $300-$800/day passive income

---

## Acquisition Channels (Prioritized by ROI)

### 1. RV/Van Storage Facilities (Highest Concentration)
**Why:** Owners pay monthly to store idle vehicles = proven idle capacity
**Calgary Facilities to Target:**
- Sentinel Storage (6+ locations - verified accessible)
- StowAway RV Storage (2801-144 Ave NE)
- Springbank Self Storage & RV's
- RV Corral Storage SE Calgary (11977 154 Ave SE)
- Sid's Storage
- StorageMart (Calgary, Okotoks, Airdrie)
- Bluebird Self Storage
- Rainbow Storage Ltd.

**Approach:**
- Visit facility offices in person (managers know long-term tenants)
- Leave professional materials at check-in kiosks
- Propose partnership: "We send you owners who need storage between rentals; you refer owners wanting to monetize"
- Offer facility managers referral fee ($100/vehicle certified)

### 2. Private Party Listings Monitoring (Most Motivated Sellers)
**Why:** Owners listing for sale are actively evaluating asset value
**Platforms to Monitor Daily:**
- **Kijiji Calgary** - Search: "Ford Transit", "Transit AWD", "Transit Medium Roof", "Transit High Roof", "Sprinter 4x4", "Sprinter AWD", "ProMaster High Roof"
- **Facebook Marketplace Calgary** - Vehicle category, filter by owner
- **AutoTrader Calgary** - Filter "Private Seller" only
- **LesPAC** (Quebec/Alberta crossover)

**Automation Setup:**
```bash
# Daily cron job concept
0 8 * * * /home/acho/scripts/monitor_listings.py \
  --keywords "Ford Transit AWD,Transit Medium Roof,Transit High Roof,Sprinter 4x4,Sprinter AWD,ProMaster High Roof" \
  --location "Calgary,Edmonton,Red Deer,Lethbridge" \
  --seller-type "private" \
  --output /home/acho/leads/daily_leads_$(date +%Y%m%d).json
```

**Outreach to Private Sellers:**
```
Subject: Alternative to selling your [Vehicle] - earn $300-800/day instead

Hi [Name],

I saw your [202X Ford Transit T-250 AWD Medium Roof] listed on [Platform]. 
Instead of selling, have you considered renting it to vetted professionals?

I run nature-office - we certify mobile office vehicles and connect them with AI consulting firms, government agencies, and field teams in Alberta who need professional workspaces on wheels.

Your exact configuration (AWD + Medium Roof) qualifies for our Executive tier: $600-800/day.
We handle: vetting, insurance, contracts, payments, and 5-pillar certification.

Interested in a 10-min call to see what your vehicle could earn?
[Calendly link]

Best,
[Name]
nature-office Partnership Team
```

### 3. Vanlife/RV Communities (High-Intent Owners)
**Calgary/Alberta Groups to Infiltrate:**
- **Facebook Groups:** "Alberta Vanlife", "Calgary Campervan Owners", "Alberta Overland", "Canadian Van Dwellers", "Ford Transit Owners Canada"
- **Reddit:** r/vancalberta, r/VanLife, r/fordtransit, r/SprinterVan, r/ProMaster
- **Forums:** Expedition Portal (Alberta section), Ford Transit USA Forum (Canadian section), Sprinter Forum
- **Meetups:** Calgary Vanlife Meetup (monthly), Alberta Overland Expo (annual)

**Approach:**
- Join as genuine participant first (2-3 weeks of engagement)
- Share valuable content: "How I calculate my van's rental ROI", "Insurance for peer-to-peer rental in Alberta"
- Soft pitch: "Some owners in our community are earning $1,500-3,000/mo renting to professionals instead of tourists"

### 4. Service & Upfit Centers (Owners Investing in Quality)
**Why:** Owners spending on solar, batteries, insulation = already building 5-pillar specs
**Calgary/Edmonton Targets:**
- **Solar/Electrical:** Go Power (Edmonton), AM Solar (Calgary dealer), Battle Born Batteries dealers
- **Insulation/Climate:** Van Compass installers, Havelock Wool dealers, Webasto/Espar heater installers
- **Connectivity:** Starlink installers, Peplink/MobileMustHave dealers, weBoost installers
- **Custom Builds:** Any local van conversion shops (rare in Calgary, more in Vancouver)

**Approach:**
- Visit shops, talk to service managers
- "Your customers who just spent $15k on solar/batteries - they could ROI in 6 months renting to professionals"
- Leave co-branded materials: "Ask your installer about nature-office certification"

### 5. Dealership Service Departments (Lease Returns & Trade-Ins)
**Why:** Dealers see owners at service intervals, know lease-end timing
**Targets:**
- Jim Pattison Lease (where our target Transit is)
- Mercedes-Benz Downtown Calgary (Sprinter specialist)
- Eastside Dodge (ProMaster volume dealer)
- Ford dealers: Country Hills Ford, Southview Ford, Northland Ford

**Approach:**
- Service manager relationships: "When Transit lessees turn in at 60k km, call us before wholesale"
- Offer: "We'll pay retail+ for certified vehicles, handle all paperwork"
- Leave materials in service waiting areas

### 6. Commercial Fleet Owners (Underutilized Assets)
**Targets:**
- Survey/engineering firms with seasonal field crews
- Film production companies (idle between shoots)
- Utility contractors (winter slowdown)
- Event companies (seasonal)

**Approach:**
- LinkedIn outreach to Fleet Managers at: Stantec, WSP, AECOM, local survey firms
- "Your 3 Transits sit idle November-March. We'll certify and rent them to AI firms - $4,000-6,000/mo per vehicle"

---

## Outreach Scripts & Templates

### Cold Email Template (Storage Facility Managers)
```
Subject: Partnership opportunity for [Facility Name] tenants

Hi [Manager Name],

I manage nature-office, Alberta's mobile office certification platform. 
We help RV/van owners monetize idle vehicles by renting to vetted professionals (AI consultants, government field teams, engineers).

Many of your tenants have vehicles sitting 20+ days/month. We'd love to:
1. Offer your tenants a no-obligation vehicle assessment (free)
2. Pay you $100 referral for each tenant vehicle we certify
3. Provide certified vehicles discounted storage when not rented

10-min call this week?
[Calendly]

[Name] | nature-office | [Phone]
```

### SMS/WhatsApp Template (Private Sellers)
```
Hi, saw your Transit AWD on Kijiji. Instead of selling, we certify & rent similar vans to professionals for $600-800/day. We handle everything. Open to a quick chat? [Name] - nature-office
```

### LinkedIn Message (Fleet Managers)
```
Hi [Name], noticed [Company] has Ford Transit AWD vans. We help firms monetize idle fleet assets by certifying them as mobile offices for professional renters ($600-800/day). Managed service - we handle vetting, insurance, logistics. Worth 10 mins?
```

---

## Qualification Checklist (Pre-Screening)

Before investing time, verify owner/vehicle meets minimum criteria:

**Vehicle Must-Haves:**
- [ ] 2020 or newer (warranty/tech relevance)
- [ ] AWD or 4x4 (Alberta climate requirement)
- [ ] Medium or High roof (workspace pillar)
- [ ] <150,000 km (reliability)
- [ ] Clean title, no major accidents
- [ ] Commercial insurance eligible

**Owner Must-Haves:**
- [ ] Owns outright or >50% equity
- [ ] Vehicle idle 3+ days/week average
- [ ] Willing to install tracking/telemetry
- [ ] Alberta-based (insurance/regulatory)
- [ ] Responsive to communication (test with initial outreach)

**Nice-to-Haves (Tier Boosters):**
- [ ] Solar system (>400W)
- [ ] Lithium battery bank (>200Ah)
- [ ] Starlink/5G router installed
- [ ] Diesel heater/Webasto
- [ ] Insulated walls/ceiling (R-value >10)
- [ ] Standing desk/monitor mount pre-installed
- [ ] Privacy curtains/window covers
- [ ] Shore power inlet

---

## Lead Tracking & Pipeline

### CRM Setup (Simple, Effective)
```
Status: New → Contacted → Qualified → Assessment Scheduled → Certified → Live on Platform
```

### Weekly Targets
- **Storage facility visits:** 3/week (rotate locations)
- **Private listing outreach:** 20 messages/week
- **Community engagement:** 5 meaningful interactions/week
- **Service center visits:** 2/week
- **Fleet outreach:** 10 LinkedIn messages/week

### Conversion Funnel Metrics
| Stage | Target Count | Conversion Rate | Time Investment |
|-------|-------------|-----------------|-----------------|
| Leads Identified | 50/week | 100% (input) | 5 hrs |
| Responses Received | 15/week | 30% | 3 hrs |
| Qualified Owners | 8/week | 53% of responses | 4 hrs |
| Assessments Booked | 5/week | 62% of qualified | 2 hrs |
| Vehicles Certified | 3/week | 60% of assessed | 6 hrs |
| **Live on Platform** | **2-3/week** | **40-60% of assessed** | Ongoing |

---

## 90-Day Sprint Plan

### Month 1: Foundation & Storage Channel
**Week 1-2:**
- [ ] Visit all 8 Calgary storage facilities, meet managers
- [ ] Set up listing monitoring automation
- [ ] Join 5 Facebook/Reddit communities, begin engagement
- [ ] Create outreach templates and Calendly booking

**Week 3-4:**
- [ ] Launch storage facility referral program
- [ ] Send first 50 private seller messages
- [ ] Visit 4 service/upfit centers
- [ ] First 3 assessments scheduled

### Month 2: Scale & Optimize
**Week 5-6:**
- [ ] Analyze response rates, optimize messaging
- [ ] Expand to Edmonton storage facilities (3 locations)
- [ ] Launch fleet manager LinkedIn campaign (50 contacts)
- [ ] Refine qualification checklist based on real data

**Week 7-8:**
- [ ] Implement referral incentives for certified owners
- [ ] Create owner success stories/content for social proof
- [ ] Automate lead scoring and follow-up sequences
- [ ] Target: 10 vehicles certified this month

### Month 3: Systematize & Expand
**Week 9-10:**
- [ ] Document full SOP for owner acquisition
- [ ] Hire/train part-time acquisition specialist (if volume >15/week)
- [ ] Build owner onboarding portal (self-serve qualification)
- [ ] Target: 15 vehicles certified this month

**Week 11-12:**
- [ ] Expand to Red Deer/Lethbridge storage corridor
- [ ] Partner with 1-2 dealerships for lease-return pipeline
- [ ] Create "Ambassador Program" for top-performing owners
- [ ] Target: 20 vehicles certified this month

---

## Budget & Resources

### Monthly Acquisition Budget
| Channel | Cost | Expected Vehicles | CAC (Customer Acquisition Cost) |
|---------|------|-------------------|--------------------------------|
| Storage facility partnerships | $500 (materials, referral fees) | 3-5 | $100-166 |
| Private listing outreach (time/tools) | $300 (automation, phone) | 2-4 | $75-150 |
| Community engagement (time) | $200 (time value) | 1-2 | $100-200 |
| Service center relationships | $200 (materials, visits) | 1-2 | $100-200 |
| Fleet LinkedIn outreach | $150 (Sales Navigator) | 1-3 | $50-150 |
| **Total** | **$1,350** | **8-16** | **$84-168** |

### Required Tools
- **Monitoring:** Custom Python script + cron (or paid: Visualping, Distill.io)
- **Outreach:** Gmail/Outlook + Streak CRM (free tier) or HubSpot Free
- **Scheduling:** Calendly (free tier)
- **Communication:** Business phone/WhatsApp Business
- **Tracking:** Airtable or Notion (free tier sufficient)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Owner ghosts after interest | Automated 3-touch follow-up sequence (Day 1, 3, 7) |
| Vehicle fails certification | Pre-screen with checklist; only book assessments for 80%+ likely |
| Insurance complications | Partner with broker specializing in peer-to-peer commercial |
| Seasonal demand fluctuation | Build pipeline 60 days ahead; maintain 2x inventory buffer |
| Owner pulls vehicle mid-rental | Contract with 30-day notice; maintain waitlist of backup vehicles |

---

## Success Definition (90 Days)

**Minimum Viable Supply:**
- **25 certified vehicles** on platform
- **Mix:** 15 Executive/Professional, 10 Office tier
- **Geography:** 20 Calgary, 5 Edmonton corridor
- **Availability:** Average 15+ rentable days/month per vehicle
- **Owner Retention:** 90%+ at 90 days

**Revenue Validation:**
- $15,000+/month in platform fees (20% take rate on $75,000 GMV)
- Proves two-sided marketplace model works
- Justifies Series A / scale funding

---

## Next Actions (This Week)

1. **Monday:** Visit Sentinel Storage Calgary Downtown & Central locations
2. **Tuesday:** Set up listing monitoring script for Kijiji/FB Marketplace
3. **Wednesday:** Join 3 Facebook groups, make 5 helpful comments
4. **Thursday:** Visit Go Power/AM Solar dealer in Calgary
5. **Friday:** Send first 20 private seller outreach messages
6. **Weekend:** Draft owner onboarding flow and certification checklist

---

*This plan is designed for execution by 1 founder/operator working 15-20 hrs/week on acquisition. All tactics are legal, compliant with Canadian anti-spam legislation (CASL), and respect platform terms of service.*