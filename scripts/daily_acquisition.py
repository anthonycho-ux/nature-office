#!/usr/bin/env python3
"""
Daily Acquisition Execution Script for nature-office
Runs all acquisition activities for a single day
"""

import sys
import os
sys.path.append('/home/acho/Projects/nature-office/scripts')

from monitor_listings import VehicleListingMonitor
from outreach_tracker import OutreachTracker
from storage_tracker import StorageFacilityTracker
from datetime import datetime

def run_daily_acquisition():
    print("=" * 60)
    print(f"NATURE-OFFICE DAILY ACQUISITION - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    # 1. Monitor vehicle listings
    print("\n[1/4] MONITORING VEHICLE LISTINGS...")
    monitor = VehicleListingMonitor()
    listings = monitor.monitor()
    print(f"     Found {len(listings)} new listings")
    
    # 2. Update outreach tracker with new leads
    print("\n[2/4] UPDATING OUTREACH TRACKER...")
    tracker = OutreachTracker()
    
    for listing in listings:
        # Check if we already have this lead
        existing = any(l["vehicle"] in listing["title"] for l in tracker.data["leads"])
        if not existing:
            tracker.add_lead(
                source=listing.get("source", "AutoTrader"),
                vehicle=listing["title"],
                owner_name=listing.get("dealer", "Unknown"),
                contact_info=listing.get("url", ""),
                notes=listing.get("notes", "")
            )
            print(f"     Added new lead: {listing['title'][:60]}...")
        else:
            print(f"     Lead already exists: {listing['title'][:60]}...")
    
    # 3. Show storage facilities to visit today
    print("\n[3/4] STORAGE FACILITY VISITS...")
    storage = StorageFacilityTracker()
    not_visited = storage.get_by_status("not_visited")
    in_progress = storage.get_by_status("in_progress")
    
    print(f"     Not visited: {len(not_visited)}")
    print(f"     In progress: {len(in_progress)}")
    
    if not_visited:
        print("\n     TODAY'S RECOMMENDED VISITS (max 3):")
        for i, facility in enumerate(not_visited[:3]):
            print(f"       {i+1}. {facility['name']}")
            print(f"          Address: {facility['address']}")
            print(f"          Phone: {facility['phone']}")
            print(f"          Notes: {facility['notes'][:80]}...")
            print()
    
    # 4. Show outreach tasks
    print("\n[4/4] OUTREACH TASKS...")
    new_leads = tracker.get_leads_by_status("new")
    contacted = tracker.get_leads_by_status("contacted")
    qualified = tracker.get_leads_by_status("qualified")
    
    print(f"     New leads to contact: {len(new_leads)}")
    print(f"     Awaiting response: {len(contacted)}")
    print(f"     Qualified - schedule assessment: {len(qualified)}")
    
    if new_leads:
        print("\n     PRIORITY OUTREACH TODAY:")
        for lead in new_leads[:5]:
            print(f"       - {lead['vehicle']} ({lead['source']})")
            print(f"         Contact: {lead['contact_info']}")
            print(f"         Template: private_seller_email")
            print()
    
    # Summary
    print("\n" + "=" * 60)
    print("DAILY SUMMARY")
    print("=" * 60)
    print(f"New listings found: {len(listings)}")
    print(f"Total leads in pipeline: {len(tracker.data['leads'])}")
    print(f"Storage facilities to visit: {len(not_visited)}")
    print(f"Outreach messages to send: {len(new_leads)}")
    print(f"\nNEXT ACTIONS:")
    print(f"  1. Visit top 3 storage facilities")
    print(f"  2. Send outreach to {len(new_leads)} new leads")
    print(f"  3. Follow up with {len(contacted)} contacted leads")
    print(f"  4. Schedule assessments for {len(qualified)} qualified leads")
    print("=" * 60)

if __name__ == "__main__":
    run_daily_acquisition()