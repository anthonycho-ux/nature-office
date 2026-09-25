#!/usr/bin/env python3
"""
Storage Facility Visit Tracker for nature-office
Manages visits to RV storage facilities to meet owners
"""

import json
import csv
from datetime import datetime
from pathlib import Path

class StorageFacilityTracker:
    def __init__(self):
        self.data_file = Path("/home/acho/Projects/nature-office/leads/storage_facilities.json")
        self.csv_file = Path("/home/acho/Projects/nature-office/leads/storage_facilities.csv")
        self.data = self.load()
    
    def load(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"facilities": self.default_facilities()}
    
    def default_facilities(self):
        return [
            {
                "id": 1,
                "name": "Sentinel Storage - Calgary Downtown",
                "address": "339 10th Avenue Southeast, Calgary, AB T2G 0W2",
                "phone": "1-833-337-7746",
                "website": "https://www.sentinel.ca/en/self-storage/calgary-rv-storage/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "Verified accessible via Lightpanda. 4.9 stars. Features: Parcel Acceptance, Climate Controlled, Drive-up, Interior Units",
                "owner_leads": []
            },
            {
                "id": 2,
                "name": "Sentinel Storage - Calgary Central",
                "address": "410 Manning Road Northeast, Calgary, AB T2E 8K4",
                "phone": "1-833-337-7746",
                "website": "https://www.sentinel.ca/en/self-storage/calgary-rv-storage/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "4.7 stars. Features: Parcel Acceptance, Heated, Drive-up, Interior Units",
                "owner_leads": []
            },
            {
                "id": 3,
                "name": "Sentinel Storage - Calgary Glenmore",
                "address": "5950 12 St SE, Calgary, AB T2H 2X2",
                "phone": "1-833-337-7746",
                "website": "https://www.sentinel.ca/en/self-storage/calgary-rv-storage/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "4.8 stars. Features: Move-in Van, Parcel Acceptance, Drive-up, Climate Controlled",
                "owner_leads": []
            },
            {
                "id": 4,
                "name": "StowAway RV Storage",
                "address": "2801-144 Ave NE, Calgary, AB",
                "phone": "587-438-3304",
                "website": "https://www.stowawayrvstorage.ca/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "Secure key-code access, pest control, clean dust-free premise",
                "owner_leads": []
            },
            {
                "id": 5,
                "name": "Springbank Self Storage & RV's",
                "address": "Springbank area, Calgary, AB",
                "phone": "",
                "website": "https://www.springbankselfstorage.com/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "Fully fenced, 24-hour video surveillance and alarm system",
                "owner_leads": []
            },
            {
                "id": 6,
                "name": "RV Corral Storage SE Calgary",
                "address": "11977 154 Ave SE, Calgary, AB",
                "phone": "587-355-6707",
                "website": "https://rvstoragecalgary.com/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "$900/year. 30' to 50' stalls available",
                "owner_leads": []
            },
            {
                "id": 7,
                "name": "Sid's Storage",
                "address": "Calgary, AB",
                "phone": "(403) 630-1415",
                "website": "https://www.sidsstorage.com/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "Affordable RV storage, secure, well-maintained",
                "owner_leads": []
            },
            {
                "id": 8,
                "name": "StorageMart",
                "address": "Calgary, Okotoks, Airdrie",
                "phone": "",
                "website": "https://www.storage-mart.com/calgary/rv-storage",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "Multiple facilities with RV storage",
                "owner_leads": []
            },
            {
                "id": 9,
                "name": "Bluebird Self Storage",
                "address": "Calgary, AB",
                "phone": "",
                "website": "https://bluebirdstorage.ca/outdoor-rv-storage-in-calgary-at-bluebird-self-storage",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "Automatic gate access, code gate entry, high-tech security",
                "owner_leads": []
            },
            {
                "id": 10,
                "name": "Rainbow Storage Ltd.",
                "address": "Calgary, AB",
                "phone": "",
                "website": "https://www.rainbowstorage.ca/",
                "contact_person": "",
                "status": "not_visited",
                "visit_date": "",
                "manager_name": "",
                "manager_email": "",
                "manager_phone": "",
                "partnership_interest": "",
                "referral_fee_agreed": False,
                "materials_left": False,
                "notes": "Indoor, covered, and outdoor storage options",
                "owner_leads": []
            }
        ]
    
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        self.export_csv()
    
    def export_csv(self):
        if not self.data["facilities"]:
            return
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "id", "name", "address", "phone", "website", "contact_person",
                "status", "visit_date", "manager_name", "manager_email", "manager_phone",
                "partnership_interest", "referral_fee_agreed", "materials_left", "notes"
            ])
            writer.writeheader()
            for facility in self.data["facilities"]:
                row = {k: v for k, v in facility.items() if k != "owner_leads"}
                writer.writerow(row)
    
    def get_facility(self, facility_id):
        for f in self.data["facilities"]:
            if f["id"] == facility_id:
                return f
        return None
    
    def update_visit(self, facility_id, **kwargs):
        facility = self.get_facility(facility_id)
        if facility:
            facility.update(kwargs)
            if "status" in kwargs:
                facility["visit_date"] = datetime.now().isoformat()
            self.save()
            return facility
        return None
    
    def get_by_status(self, status):
        return [f for f in self.data["facilities"] if f["status"] == status]
    
    def add_owner_lead(self, facility_id, owner_info):
        facility = self.get_facility(facility_id)
        if facility:
            owner_info["date_added"] = datetime.now().isoformat()
            facility["owner_leads"].append(owner_info)
            self.save()
            return True
        return False

if __name__ == "__main__":
    tracker = StorageFacilityTracker()
    print("Storage Facility Tracker initialized.")
    print(f"Total facilities: {len(tracker.data['facilities'])}")
    print(f"Data file: {tracker.data_file}")
    print(f"CSV export: {tracker.csv_file}")
    
    print("\n--- Facilities to Visit ---")
    for f in tracker.data["facilities"]:
        print(f"  {f['id']}. {f['name']} - {f['address']}")
        print(f"     Phone: {f['phone']}")
        print(f"     Status: {f['status']}")
        print()