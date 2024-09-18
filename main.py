from models import Base, Band, Venue, Concert, engine, Session

def add_sample_data(session):
    # Create band and venue
    band = Band(name='The Leopards', hometown='Lavi')
    venue = Venue(title='GMC', city='Nairobi')
    
    # Add band and venue to session 
    session.add(band)
    session.add(venue)
    session.commit()  # Commit to generate IDs
    
    # create a concert with existing band and venue
    concert = Concert(date='2024-09-18', band_id=band.id, venue_id=venue.id)

    # Add concert to session
    session.add(concert)
    session.commit()

def query_and_print_data(session):
    # Query and print data
    for concert in session.query(Concert).all():
        print(f"Date: {concert.date}, Band: {concert.band.name}, Venue: {concert.venue.title}")

def test_relationships():
    # Fetching a band and a venue
    band = session.query(Band).first()
    venue = session.query(Venue).first()
    
    # check to ensure we have data
    if not band or not venue:
        print("No data found.")
        return
    
    # Print concerts band
    print("Band's concerts:", [c.date for c in band.get_concerts()])
    
    # Print concerts venue
    print("Venue's concerts:", [c.date for c in venue.get_concerts()])
    
    # Print all bands at the venue
    print("Bands at venue:", [b.name for b in venue.get_bands()])
    
    # Print all venues where the band has performed
    print("Venues for band:", [v.title for v in band.get_venues()])  # Use the venues() method
    # Close the session
    session.close()

if __name__ == "__main__":
    # Create the database tables
    Base.metadata.create_all(engine)
    
    # Create a new session and add sample data
    session = Session()
    add_sample_data(session)
    
    # Query and print data
    query_and_print_data(session)
    
    # Run the test
    test_relationships()