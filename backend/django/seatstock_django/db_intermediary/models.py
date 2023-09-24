from django.db import models

class School(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    football_stadium_name = models.CharField(max_length=100)
    football_stadium_location = models.CharField(max_length=200)
    team_name = models.CharField(max_length=100)
    state = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Game(models.Model):
    home_team = models.ForeignKey(School, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(School, on_delete=models.CASCADE, related_name="away_team")
    date = models.DateTimeField()
    is_womens_game = models.BooleanField()
    is_mens_game = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['home_team', 'away_team', 'date'], name="Game_PK"
            )
        ]

    def __str__(self):
        return self.home + " vs " + self.away_team
    

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    school_email = models.CharField(max_length=200, primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    phone_number_country_code = models.IntegerField()
    phone_number = models.IntegerField()
    password_string = models.CharField(max_length=200)
    is_banned = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)
    account_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=255, primary_key=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ask = models.FloatField()
    seat = models.IntegerField()
    row = models.IntegerField()
    section = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.ticket_id

class Bid(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    is_active = models.BooleanField()
    is_accepted = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["buyer", "ticket", "amount"], name="Bid_PK"
            )
        ]

    def __str__(self):
        return self.buyer + " offering " + self.amount + " for " + self.ticket
    
class Transaction(models.Model):
    transaction_id = models.BigIntegerField(primary_key=True)
    bid = models.ForeignKey(Bid, on_delete=models.DO_NOTHING)
    transaction_fee = models.FloatField()
    processing_fee = models.FloatField()
    seller_accepted = models.BooleanField(default=False)
    buyer_sent_payment = models.BooleanField(default=False)
    seller_sent_payment = models.BooleanField(default=False)
    buyer_confirmed_payment = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_id
    
class Sale(models.Model):
    sale_id = models.BigIntegerField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)
    total_amount = models.FloatField()
    date = models.DateTimeField()
    complaint_period_end_date = models.DateTimeField()

    def __str__(self):
        return self.sale_id
    
class Complaint(models.Model):
    initiating_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    sale = models.ForeignKey(Sale, on_delete=models.DO_NOTHING)
    accuser_provided_proof = models.BooleanField(default=False)
    accuser_provided_proof_at = models.DateTimeField()
    defendant_contacted = models.BooleanField(default=False)
    defendant_contacted_at = models.DateTimeField()
    defendant_provided_proof = models.BooleanField(default=False)
    defendant_provided_proof_at = models.DateTimeField()
    accuser_refunded = models.BooleanField(default=False)
    accuser_refunded_at = models.DateTimeField()
    defendant_exonerated = models.BooleanField()
    defendant_exonerated_at = models.DateTimeField()
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['initiating_user', 'sale'], name="Complaint_PK"
            )
        ]

    def __str__(self):
        return self.initiating_user + " on " + self.sale