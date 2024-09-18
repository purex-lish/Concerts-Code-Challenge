from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String)
    
    concerts = relationship('Concert', back_populates='band')
    
    def play_in_venue(self, venue, date):
        """"Creates a new concert for the band in the specified venue on the given date."""
        new_concert = Concert(band=self, venue=venue, date=date)
        session.add(new_concert)
        session.commit()
        
    def all_introductions(self):
        """Returns an array of strings representing all the introductions for this band."""
        return [concert.introduction() for concert in self.concerts]
    
    @classmethod
    def most_performances(cls):
        """Returns the band with the most concerts."""
        bands = session.query(cls).all()
        band_performance_counts = {band: len(band.concerts) for band in bands}
        return max(band_performance_counts, key=band_performance_counts.get)

    def get_concerts(self):
        """Returns all concerts for this band."""
        return self.concerts
    
    def get_venues(self):
        """Returns all venues where this band has performed."""
        return [concert.venue for concert in self.concerts]

class Venue(Base):
    __tablename__ = 'venues'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String)
    concerts = relationship('Concert', back_populates='venue')
    
    def concert_on(self, date):
        """Finds and returns the first concert on the given date at this venue."""
        return session.query(Concert).filter_by(venue=self, date=date).first()

    def most_frequent_band(self):
        """Returns the band with the most concerts at this venue."""
        band_counts = {}
        for concert in self.concerts:
            band = concert.band
            if band in band_counts:
                band_counts[band] += 1
            else:
                band_counts[band] = 1
        return max(band_counts, key=band_counts.get)
    
    def get_concerts(self):
        """Returns all concerts at this venue."""
        return self.concerts
    
    def get_bands(self):
        """Returns all bands who have performed at this venue."""
        return [concert.band for concert in self.concerts]

class Concert(Base):
    __tablename__ = 'concerts'
    
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    band_id = Column(Integer, ForeignKey('bands.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    
    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')
    
    def hometown_show(self):
        """Returns True if the concert is in the band's hometown, false otherwise."""
        return self.venue.city == self.band.hometown
    
    def introduction(self):
        """Returns a string with the bands's introduction for this concert."""
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
    
# Set up the engine and session
engine = create_engine('sqlite:///concerts.db')  # Use your preferred database
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)