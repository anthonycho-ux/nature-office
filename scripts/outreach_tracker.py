#!/usr/bin/env python3
"""
Owner Outreach Tracker for nature-office
Helps manage and track outreach to individual vehicle owners
"""

import json
import csv
from datetime import datetime
from pathlib import Path

class OutreachTracker:
    def __init__(self):
        self.data_file = Path("/home/acho/Projects/nature-office/leads/outreach_tracker.json")
        self.csv_file = Path("/home/acho/Projects/nature-office/leads/outreach_tracker.csv")
        self.data = self.load()
    
    def load(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"leads": [], "templates": self.default_templates()}
    
    def default_templates(self):
        return {
            "private_seller_email": """Subject: Alternative to selling your {vehicle} - earn $300-800/day instead

Hi {name},

I saw your {vehicle} listed on {platform}. 
Instead of selling, have you considered renting it to vetted professionals?

I run nature-office - we certify mobile office vehicles and connect them with AI consulting firms, government agencies, and field teams in Alberta who need professional workspaces on wheels.

Your exact configuration ({key_features}) qualifies for our {tier} tier: ${daily_rate}/day.
We handle: vetting, insurance, contracts, payments, and 5-pillar certification.

Interested in a 10-min call to see what your vehicle could earn?
{calendly_link}

Best,
{my_name}
nature-office Partnership Team""",
            
            "storage_manager_email": """Subject: Partnership opportunity for {facility_name} tenants

Hi {manager_name},

I manage nature-office, Alberta's mobile office certification platform. 
We help RV/van owners monetize idle vehicles by renting to vetted professionals (AI consultants, government field teams, engineers).

Many of your tenants have vehicles sitting 20+ days/month. We'd love to:
1. Offer your tenants a no-obligation vehicle assessment (free)
2. Pay you $100 referral for each tenant vehicle we certify
3. Provide certified vehicles discounted storage when not rented

10-min call this week?
{calendly_link}

{my_name} | nature-office | {phone}""",
            
            "sms_private_seller": "Hi, saw your {vehicle} on {platform}. Instead of selling, we certify & rent similar vans to professionals for ${daily_rate}/day. We handle everything. Open to a quick chat? {my_name} - nature-office",
            
            "linkedin_fleet": "Hi {name}, noticed {company} has {vehicle_type} vans. We help firms monetize idle fleet assets by certifying them as mobile offices for professional renters (${daily_rate}/day). Managed service - we handle vetting, insurance, logistics. Worth 10 mins?"
        }
    
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        self.export_csv()
    
    def export_csv(self):
        """Export to CSV for easy viewing"""
        if not self.data["leads"]:
            return
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id", "source", "owner_name", "vehicle", "contact_info", 
                "status", "created_date", "last_contact", "next_action",
                "notes", "qualification_score"
            ])
            writer.writeheader()
            for lead in self.data["leads"]:
                writer.writerow(lead)
    
    def add_lead(self, source, vehicle, owner_name="", contact_info="", notes=""):
        lead = {
            "id": len(self.data["leads"]) + 1,
            "source": source,
            "owner_name": owner_name,
            "vehicle": vehicle,
            "contact_info": contact_info,
            "status": "new",
            "created_date": datetime.now().isoformat(),
            "last_contact": "",
            "next_action": "Initial outreach",
            "notes": notes,
            "qualification_score": 0
        }
        self.data["leads"].append(lead)
        self.save()
        return lead
    
    def update_lead(self, lead_id, **kwargs):
        for lead in self.data["leads"]:
            if lead["id"] == lead_id:
                lead.update(kwargs)
                if "status" in kwargs:
                    lead["last_contact"] = datetime.now().isoformat()
                self.save()
                return lead
        return None
    
    def get_leads_by_status(self, status):
        return [l for l in self.data["leads"] if l["status"] == status]
    
    def get_template(self, template_name):
        return self.data["templates"].get(template_name, "")
    
    def render_template(self, template_name, **kwargs):
        template = self.get_template(template_name)
        for key, value in kwargs.items():
            template = template.replace(f"{{{key}}}", value)
        return template

# Demo usage
if __name__ == "__main__":
    tracker = OutreachTracker()
    
    # Add the lead we found from AutoTrader monitoring
    tracker.add_lead(
        source="AutoTrader Calgary",
        vehicle="2025 Ford Transit T-250 AWD Medium Roof",
        owner_name="Jim Pattison Lease (Dealer)",
        contact_info="Dealership: 1-833-337-7746",
        notes="Dealer listing - ask about lease returns or trade-ins with similar specs. This is a dealer, not private owner, but they know private owners trading in similar vehicles."
    )
    
    # Add a template private seller lead (placeholder for when we find them)
    tracker.add_lead(
        source="Kijiji Calgary (manual monitoring)",
        vehicle="2023 Ford Transit T-250 AWD High Roof",
        owner_name="[Private Seller - to be identified]",
        contact_info="[To be captured from listing]",
        notes="Monitor Kijiji daily for this listing. When found, use private_seller_email template."
    )
    
    print("Outreach tracker initialized with initial leads.")
    print(f"Data file: {tracker.data_file}")
    print(f"CSV export: {tracker.csv_file}")
    
    # Show email template for private seller
    print("\n--- Private Seller Email Template ---")
    print(tracker.render_template("private_seller_email", 
        name="John",
        vehicle="2023 Ford Transit T-250 AWD High Roof",
        platform="Kijiji",
        key_features="AWD + High Roof + Solar + Starlink",
        tier="Executive",
        daily_rate="600-800",
        calendly_link="https://calendly.com/nature-office/10min",
        my_name="Your Name"
    ))