from database import db

class CVEEntry(db.Model):
    id          = db.Column(db.String, primary_key=True)
    vendor      = db.Column(db.String, index=True)
    product     = db.Column(db.String)
    version     = db.Column(db.String)
    description = db.Column(db.Text)
    cvss_score  = db.Column(db.String)

    def to_dict(self):
        return {
            "id":           self.id,
            "vendor":       self.vendor,
            "product":      self.product,
            "version":      self.version,
            "description":  self.description,
            "cvss_score":   self.cvss_score
        }
